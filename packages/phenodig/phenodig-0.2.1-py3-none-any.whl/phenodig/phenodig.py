import os
import glob
import io
import requests
import logging
import warnings
import statistics
import math
from pathlib import Path
from importlib import resources

import numpy as np
import pandas as pnd
from scipy.optimize import curve_fit


import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


from .growthmodels import *




def collect_raw_data(logger, input_folder, pms, replicates, discarding):
    logger.info(f"Collecting raw data...")
    
    
    # check file presence
    files = glob.glob(f'{input_folder}/*.xlsx')
    if len(files) == 0:
        logger.error(f"No .xlsx file found in the provided directory ('--input {input_folder}').")
        return 1
    
    
    # format discarding: 
    formatted_discarding = []
    for d in discarding.split(','):
        try: 
            strain, pm, replicate = d.split('-')
            formatted_discarding.append(f"{strain} {pm} 590 {replicate}")
            formatted_discarding.append(f"{strain} {pm} 750 {replicate}")
        except:
            logger.error(f"Invalid syntax found ('--discarding {discarding}').")
            return 1
    discarding = formatted_discarding
            
    
    # each strain has its own xlsx file: 
    strain_to_df = {}
    for file in files:
        strain = Path(file).stem

        res_df = []
        excel_file = pnd.ExcelFile(file, engine='openpyxl')
        for time in range(len(excel_file.sheet_names)):
            df = excel_file.parse(f'T{time}')
            for pm in pms.split(','):
                for od in ['590', '750']:
                    for replicate in replicates.split(','):
                        readout = f'{pm} {od} {replicate}'
                        if strain + ' ' + readout in discarding:   # discard these samples
                            logger.debug(f"Discarding readout as requested: '{strain}', PM '{pm}', OD '{od}', replicate '{replicate}', time 'T{time}'.")
                            continue 

                            
                        # find boolean mask where value matches
                        mask = df == readout
                        # get the integer positions (row and column indices)
                        indices = list(zip(*mask.to_numpy().nonzero()))
                        # get the only result
                        try: result = indices[0]
                        except: 
                            logger.debug(f"Expected readout not found: strain '{strain}', PM '{pm}', OD '{od}', replicate '{replicate}', time 'T{time}'.")
                            continue


                        # adjust indices
                        row_i = result[0] + 2
                        col_i = result[1] + 1
                        for pm_row_i, pm_row in enumerate([r for r in 'ABCDEFGH']):
                            for pm_col_i, pm_col in enumerate([c +1 for c in range(12)]):
                                # get proper well name
                                pm_col = str(pm_col)
                                if len(pm_col) == 1: pm_col = '0' + pm_col
                                well = f'{pm_row}{pm_col}'
                                # get proper plate name
                                plate = pm
                                if plate == 'PM1': pass
                                if plate == 'PM2': plate = 'PM2A'
                                if plate == 'PM3': plate = 'PM3B'
                                if plate == 'PM4': plate = 'PM4A'
                                # read value
                                value = df.iloc[row_i + pm_row_i, col_i + pm_col_i]
                                res_df.append({
                                    'index_col': f"{plate}_{time}_{od}_{replicate}_{well}",
                                    'pm': plate, 'time': time, 'od': od, 'replicate': replicate, 'well': well, 'value': value})                     
        res_df = pnd.DataFrame.from_records(res_df)
        res_df = res_df.set_index('index_col', drop=True, verify_integrity=True)

        # populate dictionary
        strain_to_df[strain] = res_df
        
        
        # verbose logging
        logger.debug(f"Strain '{strain}' has {len(res_df['pm'].unique())} plates, {len(res_df['replicate'].unique())} replicates, and {len(res_df['time'].unique())} time points.")
        
        
    logger.info(f"Found {len(strain_to_df)} strains in input.")
    return strain_to_df



def data_preprocessing(logger, strain_to_df, output_folder):
    
    
    
    # step 1: OD590 - OD750:
    logger.info(f"Substracting wavelengths...")
    for i, strain in enumerate(strain_to_df.keys()):
        df = strain_to_df[strain]
        logger.debug(f"Processing strain '{strain}'...")
        
        df['value_norm'] = None   
        for index, row in df.iterrows(): 
            if row['od'] == '590':
                index_750 = f"{row['pm']}_{row['time']}_750_{row['replicate']}_{row['well']}"
                df.loc[index, 'value_norm'] = df.loc[index, 'value'] - df.loc[index_750, 'value']
        df = df[df['value_norm'].isna()==False]
        df = df.drop(columns=['od', 'value'])
        df.index = [f"{row['pm']}_{row['time']}_{row['replicate']}_{row['well']}" for index, row in df.iterrows()]
        
        strain_to_df[strain] = df

        
        
    # step 2: subtraction of the blank
    logger.info(f"Substracting negative controls...")
    for i, strain in enumerate(strain_to_df.keys()):
        df = strain_to_df[strain]
        logger.debug(f"Processing strain '{strain}'...")
        
        for index, row in df.iterrows():
            # get the well of the blank
            if row['pm'] in ['PM1', 'PM2A', 'PM3B']:
                well_black = 'A01'
            else:  # PM4A is both for P and S
                if row['well'][0] in ['A','B','C','D','E']:
                    well_black = 'A01'  # P
                else: well_black = 'F01'  # S
            # get the index of the blank
            index_blank = f"{row['pm']}_{row['time']}_{row['replicate']}_{well_black}"
            df.loc[index, 'value_norm'] = df.loc[index, 'value_norm'] - df.loc[index_blank, 'value_norm']
            if df.loc[index_blank, 'value_norm'] < 0: 
                df.loc[index_blank, 'value_norm'] = 0
                
        strain_to_df[strain] = df


        
    # step 3: substraction of T0
    logger.info(f"Substracting T0...")
    for i, strain in enumerate(strain_to_df.keys()):
        df = strain_to_df[strain]
        logger.debug(f"Processing strain '{strain}'...")
        
        for index, row in df.iterrows():
            index_T0 = f"{row['pm']}_0_{row['replicate']}_{row['well']}"
            df.loc[index, 'value_norm'] = df.loc[index, 'value_norm'] - df.loc[index_T0, 'value_norm']
            if df.loc[index_blank, 'value_norm'] < 0: 
                df.loc[index_blank, 'value_norm'] = 0
                
    strain_to_df[strain] = df


    
    # step 4: get mean +- sem given replicates
    logger.info(f"Computing mean and SEM...")
    for i, strain in enumerate(strain_to_df.keys()):
        df = strain_to_df[strain]
        logger.debug(f"Processing strain '{strain}'...")
        
        found_reps = list(df['replicate'].unique())
        df['value_mean'] = None   # dedicated column
        df['value_sem'] = None   # dedicated column
        for index, row in df.iterrows():
            values = []
            for rep in found_reps:
                index_rep = f"{row['pm']}_{row['time']}_{rep}_{row['well']}"
                try: value = df.loc[index_rep, 'value_norm']
                except: continue  # replicate missing for some reason
                values.append(value)
            if len(values) > 1:
                # get the # standard error of the mean (standard deviation)
                std_dev = statistics.stdev(values)
                sem = std_dev / math.sqrt(len(values))
                df.loc[index, 'value_mean'] = statistics.mean(values)
                df.loc[index, 'value_sem'] = sem
            else:  # no replicates
                df.loc[index, 'value_mean'] = df.loc[index, 'value_norm']
                df.loc[index, 'value_sem'] = 0
        df = df.drop(columns=['replicate', 'value_norm'])
        df = df.drop_duplicates()
        df.index = [f"{row['pm']}_{row['time']}_{row['well']}" for index, row in df.iterrows()]

        strain_to_df[strain] = df
        
        
    
    # step 5: save long tables
    os.makedirs(f'{output_folder}/tables/', exist_ok=True)
    for i, strain in enumerate(strain_to_df.keys()):
        strain_to_df[strain].to_excel(f'{output_folder}/tables/preproc_{strain}.xlsx')
        logger.info(f"'{output_folder}/tables/preproc_{strain}.xlsx' created!")
        
        
    return strain_to_df



def curve_fitting(logger, output_folder, strain_to_df, threshold_auc, plotfits):
    logger.info(f"Fitting signals...")
    zoom = 1.2
    
    
    # load official mappings
    official_pm_tables = {}
    for pm in ['PM1', 'PM2A', 'PM3B', 'PM4A']:
        with resources.path("phenodig.assets", f"{pm}.csv") as asset_path: 
            official_pm_tables[pm] = pnd.read_csv(asset_path, index_col=1, names=['plate','substrate','source','u1','u2','u3','u4','kc','cas'])
    
    
    
    strain_to_fitdf = {}
    
    # iterate strains:
    for strain, df in strain_to_df.items():
        logger.debug(f"Processing strain '{strain}'...")
        os.makedirs(f'{output_folder}/tables/', exist_ok=True)
        if plotfits: os.makedirs(f'{output_folder}/plotfits/', exist_ok=True)
        strain_to_fitdf[strain] = None


        fitdf = []
        for pm in df['pm'].unique():
            df_pm = df[df['pm']==pm]


            for i, row in enumerate('ABCDEFGH'):
                for j, col in enumerate([i+1 for i in range(12)]):
                    col = str(col)
                    if len(col)==1: col = f'0{col}'
                    well = f'{row}{col}'
                    substrate = official_pm_tables[pm].loc[well, 'substrate']
                    
                    
                    new_row = {
                        'index_col': f'{strain}_{pm}_{well}',
                        'strain': strain, 'pm': pm, 'well': well,
                        'substrate': substrate
                    }
                    
                    if (well=='A01' and pm in ['PM1', 'PM2A', 'PM3B']) \
                        or (well in ['A01', 'F01'] and pm=='PM4A'):   # handle blanks
                        fitdf.append(new_row)
                        continue
                        
                        
                    


                    # main plots: 
                    time = df_pm[df_pm['well']==well]['time'].to_numpy()
                    od = df_pm[df_pm['well']==well]['value_mean'].to_numpy()
                    
                    if plotfits:
                        fig, ax = plt.subplots(
                            nrows=1, ncols=1,
                            figsize=(12*zoom, 8*zoom), 
                            gridspec_kw={'width_ratios': [1]}
                        ) 
                        plt.subplots_adjust(wspace=0, hspace=0)
                        ax.plot(time, od, 'o', label='experimental')
                    
                    
                    
                    # get the area under the curve: 
                    auc = round(np.trapz(od, time),2)
                    new_row['auc'] = auc
                    
                    # growth calling
                    call = auc >= threshold_auc
                    new_row['call'] = call
        
                                  
                    
                    # iterate growth models: 
                    for model_id, model_f in zip(
                        ['three_phase_linear', 'four_phase_linear', 'gompertz', 'logistic', 'richards', 'baranyi', 'baranyi_nolag', 'baranyi_nostat'],
                        [three_phase_linear,   four_phase_linear, gompertz,   logistic,   richards,   baranyi,   baranyi_nolag,   baranyi_nostat]):


                        # provide initial guess for model's parameters:
                        guess_t_lag, guess_od_lag, guess_t_max, guess_t_death, guess_od_max = \
                            guess_params(time, od, n_bins=7)

                        if model_id == 'three_phase_linear': 
                            p0 = [min(od), guess_t_lag, 4.0, guess_od_max, guess_t_max]
                        elif model_id=='four_phase_linear':
                            p0 = [min(od), guess_t_lag, 4.0, guess_od_max, guess_t_max, guess_t_death, 4.0]
                        elif model_id in ['gompertz', 'logistic', 'baranyi']:
                            p0 = [min(od), guess_t_lag, 4.0, guess_od_max]
                        elif model_id=='richards':
                            p0 = [min(od), guess_t_lag, 4.0, guess_od_max, 0.1]
                        elif model_id=='baranyi_nolag':
                            p0 = [min(od), 4.0, guess_od_max]
                        elif model_id=='baranyi_nostat':
                            p0 = [min(od), guess_t_lag, 4.0]


                            
                        
                        # do the real fitting: 
                        try:
                            with warnings.catch_warnings():
                                warnings.simplefilter("ignore")

                                # predict model's parameters: 
                                params, _ = curve_fit(model_f, time, od, p0=p0, maxfev=5000)

                                # predict values using the parametrized model:
                                od_pred = model_f(time, *params)
                        except: # eg "RuntimeError: Optimal parameters not found: Number of calls to function has reached maxfev = 5000."
                            continue  # try next model
                    
                        
                            
                            
                        # extract parameters: 
                        if model_id == 'three_phase_linear': 
                            y0, t_lag, mu, ymax, t_max = params
                            t_death, mu_death, shape = None, None, None
                        elif model_id=='four_phase_linear':
                            y0, t_lag, mu, ymax, t_max, t_death, mu_death = params
                            shape = None
                        elif model_id in ['gompertz', 'logistic', 'baranyi']:
                            y0, t_lag, mu, ymax = params
                            t_max, t_death, mu_death, shape = None, None, None, None
                        elif model_id=='richards':
                            y0, t_lag, mu, ymax, shape = params
                            t_max, t_death, mu_death = None, None, None
                        elif model_id=='baranyi_nolag':
                            y0, mu, ymax = params
                            t_lag, t_max, t_death, mu_death, shape = None, None, None, None, None
                        elif model_id=='baranyi_nostat':
                            y0, t_lag, mu = params
                            ymax, t_max, t_death, mu_death, shape = None, None, None, None, None
                            
                        new_row[f'od0_{model_id}'] = y0
                        new_row[f'tlag_{model_id}'] = t_lag
                        new_row[f'mu_{model_id}'] = mu
                        new_row[f'odmax_{model_id}'] = ymax
                        new_row[f'tmax_{model_id}'] = t_max
                        new_row[f'tdeath_{model_id}'] = t_death
                        new_row[f'mudeath_{model_id}'] = mu_death
                        new_row[f'shape_{model_id}'] = shape


                        
                        # compute metrics:
                        r2 = R2(od, od_pred)
                        n_params = len(inspect.signature(model_f).parameters) -2  # '-2' becaue of 't' and 't0'
                        aic = AIC(od, od_pred, n_params)
                        
                        new_row[f'R2_{model_id}'] = r2
                        new_row[f'AIC_{model_id}'] = aic
                        
                        
                        
                        
                        if plotfits:
                            # draw the curve (more time points: smoother)
                            with warnings.catch_warnings():
                                warnings.simplefilter("ignore")
                                x = get_more_t_point(time, mult=100)
                                y = model_f(x, *params)
                            ax.plot(x, y, '--', label=f'{model_id} (R2={r2}; AIC={aic})')
                            
                        
                    fitdf.append(new_row)
                    
                    if plotfits:
                        ax.set_xlabel('time')
                        ax.set_ylabel('processed signal')
                        ax.set_title(f'bacterial growth models\nstrain: {strain} PM: {pm} well: {well}')
                        ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
                        ax.grid(True)
                        plt.savefig(f'{output_folder}/plotfits/{pm}_{well}_{strain}.png', dpi=200, bbox_inches='tight') 
                        plt.close(fig)  

                    
        
        # populate dict:
        fitdf = pnd.DataFrame.from_records(fitdf)
        fitdf = fitdf.set_index('index_col', drop=True, verify_integrity=True)
        sorted_cols = set(list(fitdf.columns)) - set(['strain', 'pm', 'well', 'substrate', 'auc', 'call'])
        sorted_cols = sorted(list(sorted_cols))
        sorted_cols = ['strain', 'pm', 'well', 'substrate', 'auc', 'call'] + sorted_cols
        fitdf = fitdf[sorted_cols]  # columns by alphabetical order
        strain_to_fitdf[strain] = fitdf
        
        # save table:
        fitdf_xlsx = fitdf.fillna('na')
        fitdf_xlsx = fitdf_xlsx.reset_index(drop=True)
        fitdf_xlsx.index = fitdf_xlsx.index +1
        fitdf_xlsx.to_excel(f'{output_folder}/tables/fitting_{strain}.xlsx')
        logger.info(f"'{output_folder}/tables/fitting_{strain}.xlsx' created!")


    return strain_to_fitdf



def plot_plates(logger, output_folder, strain_to_df, strain_to_fitdf, noynorm, threshold_auc):
        
    zoom = 1.2
    logger.info(f"Plotting PM plates...")


    # load official mappings
    official_pm_tables = {}
    for pm in ['PM1', 'PM2A', 'PM3B', 'PM4A']:
        with resources.path("phenodig.assets", f"{pm}.csv") as asset_path: 
            official_pm_tables[pm] = pnd.read_csv(asset_path, index_col=1, names=['plate','substrate','source','u1','u2','u3','u4','kc','cas'])
    

    # get global y min/max
    if noynorm == False:
        mins, maxs = [], []
        for strain, df in strain_to_df.items():
            mins.append(min(df['value_mean'] - df['value_sem']))
            maxs.append(max(df['value_mean'] + df['value_sem']))
        y_min, y_max = min(mins), max(maxs)


    # iterate strains:
    os.makedirs(f'{output_folder}/figures/', exist_ok=True)
    for strain, df in strain_to_df.items():
        for pm in df['pm'].unique():
            df_pm = df[df['pm']==pm]


            # prepare subplots:
            fig, axs = plt.subplots(
                nrows=8, ncols=12,
                figsize=(12*zoom, 8*zoom), 
                gridspec_kw={'width_ratios': [1 for i in range(12)]}
            ) 
            plt.subplots_adjust(wspace=0, hspace=0)


            # get min and max: 
            if noynorm:
                y_min = min(df_pm['value_mean'] - df_pm['value_sem'])  
                y_max = max(df_pm['value_mean'] + df_pm['value_sem'])


            for i, row in enumerate('ABCDEFGH'):
                for j, col in enumerate([i+1 for i in range(12)]):
                    col = str(col)
                    if len(col)==1: col = f'0{col}'
                    well = f'{row}{col}'


                    # main plots: 
                    x_vector = df_pm[df_pm['well']==well]['time'].to_list()
                    y_vector = df_pm[df_pm['well']==well]['value_mean'].to_list()
                    sem_vector = df_pm[df_pm['well']==well]['value_sem'].to_list()
                    y_vector_eneg = [y-e if (y-e)>=0 else 0 for y,e in zip(y_vector, sem_vector) ]
                    y_vector_epos = [y+e if (y+e)>=0 else 0 for y,e in zip(y_vector, sem_vector) ]


                    axs[i, j].scatter(x_vector, y_vector, s=10, color='C0')
                    axs[i, j].plot(x_vector, y_vector, linestyle='-', color='C0')
                    axs[i, j].fill_between(x_vector, y_vector, color='C0', edgecolor=None, alpha=0.4)
                    axs[i, j].fill_between(x_vector, y_vector_eneg, y_vector_epos, color='grey', edgecolor=None, alpha=0.5)


                    # normalize axis limit: 
                    axs[i, j].set_ylim(y_min, y_max)
                    axs[i, j].set_xlim(left=0)  

                    
                    with warnings.catch_warnings():
                        # avoid "UserWarning: set_ticklabels() should only be used with a fixed number of ticks, i.e. after set_ticks() or using a FixedLocator."
                        warnings.simplefilter("ignore")
                        
                        # set ticks:
                        axs[i, j].xaxis.set_major_locator(MaxNLocator(nbins=5, integer=True))  
                        axs[i, j].yaxis.set_major_locator(MaxNLocator(nbins=5)) 
                        
                        # set tick labels (exclude 0)
                        axs[i, j].set_xticklabels([str(int(i)) if i!=0 else '' for i in axs[i, j].get_xticks()])
                        axs[i, j].set_yticklabels([str(i) if i!=0 else '' for i in axs[i, j].get_yticks()])

                        # remove ticks for central plots
                        if j!=0: axs[i, j].set_yticks([])
                        if i!=7: axs[i, j].set_xticks([])
                        


                    # set background color
                    call = strain_to_fitdf[strain].loc[f'{strain}_{pm}_{well}', 'call']
                    bg_color = 'white'
                    if call: 
                        bg_color = '#f0ffdb'  # paler green
                    else: 
                        bg_color = 'mistyrose'
                    axs[i, j].set_facecolor(bg_color)




                    # annotations:
                    color = 'grey'
                    padx, pady = max(x_vector)/40, y_max/10
                    
                    # title
                    axs[i, j].text(padx, y_max - pady*0 -pady/2, well, fontsize=7, fontweight='bold', ha='left', va='top', color=color)
                    
                    # substrate name
                    annot_substrate = official_pm_tables[pm].loc[well, 'substrate']
                    if len(annot_substrate) > 15: annot_substrate = annot_substrate[0:15] + '...'
                    annot_substrate = f'{annot_substrate}'
                    axs[i, j].text(padx, y_max - pady*1 -pady/2, annot_substrate, fontsize=7, ha='left', va='top', color=color)
                    
                    # substrate kc
                    annot_kc = official_pm_tables[pm].loc[well, 'kc']
                    if type(annot_kc)==float : annot_kc = 'na'
                    annot_kc = f'kc: {annot_kc}'
                    axs[i, j].text(padx, y_max - pady*2 -pady/2, annot_kc, fontsize=6, ha='left', va='top', color=color)

                    # call parameters:
                    auc = strain_to_fitdf[strain].loc[f'{strain}_{pm}_{well}', 'auc']
                    annot_auc = f'AUC: {auc}'
                    axs[i, j].text(padx, y_max - pady*3 -pady/2, annot_auc, fontsize=6, ha='left', va='top', color=color)


            # set main title:
            fig.suptitle(f'{strain} - Biolog® {pm}  (thr={threshold_auc})', y=0.9)
            plt.savefig(f'{output_folder}/figures/{pm}_{strain}.png', dpi=200, bbox_inches='tight') 
            plt.close(fig)  
        logger.info(f"'{output_folder}/figures/*_{strain}.png' created!")

        
        
def phenodig(args, logger): 
    
    
    # adjust out folder path
    while args.output.endswith('/'):
        args.output = args.output[:-1]
    
        
    strain_to_df = collect_raw_data(logger, args.input, args.plates, args.replicates, args.discarding)
    if type(strain_to_df) == int: return 1


    strain_to_df = data_preprocessing(logger, strain_to_df, args.output)
    if type(strain_to_df) == int: return 1


    strain_to_fitdf = curve_fitting(logger, args.output, strain_to_df, args.auc, args.plotfits)
    if type(strain_to_fitdf) == int: return 1


    response = plot_plates(logger, args.output, strain_to_df, strain_to_fitdf, args.noynorm, args.auc)
    if response==1: return 1
    
        
    return 0