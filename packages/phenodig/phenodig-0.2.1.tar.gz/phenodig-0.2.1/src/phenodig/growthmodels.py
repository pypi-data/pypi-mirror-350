import statistics
import inspect


import numpy as np




def three_phase_linear(t, y0, t_lag, mu, ymax, t_max):
    y0 = 0   # due to the imposed preprocessing, y0==0 always.
    return np.piecewise(
        t, [t<=t_lag, (t>t_lag) & (t<=t_max), t>t_max],
        [lambda t: y0, lambda t: y0+mu*(t-t_lag), lambda t: y0+mu*(t_max-t_lag)])

def four_phase_linear(t, y0, t_lag, mu, ymax, t_max, t_death, mu_death):
    y0 = 0   # due to the imposed preprocessing, y0==0 always.
    return np.piecewise(
        t, [t<=t_lag, (t>t_lag) & (t<=t_max), (t>t_max) & (t<=t_death), t>t_death], 
        [lambda t: y0, lambda t: y0+mu*(t-t_lag), lambda t: y0+mu*(t_max-t_lag), lambda t: y0+mu*(t_max-t_lag)-mu_death*(t-t_death)])

def gompertz(t, y0, t_lag, mu, ymax):
    y0 = 0   # due to the imposed preprocessing, y0==0 always.
    # rewritten with biologial parameters by ZWIETERING et al, 1990 (doi 10.1128/aem.56.6.1875-1881.1990).
    return (ymax * np.exp(-np.exp((mu * np.e / ymax) * (t_lag - t) + 1))) + y0

def logistic(t, y0, t_lag, mu, ymax):
    y0 = 0   # due to the imposed preprocessing, y0==0 always.
    # rewritten with biologial parameters by ZWIETERING et al, 1990 (doi 10.1128/aem.56.6.1875-1881.1990).
    return (ymax / (1 + np.exp(4*mu / ymax * (t_lag - t) +2))) + y0

def richards(t, y0, t_lag, mu, ymax, shape):
    y0 = 0   # due to the imposed preprocessing, y0==0 always.
    # rewritten with biologial parameters by ZWIETERING et al, 1990 (doi 10.1128/aem.56.6.1875-1881.1990).
    return (ymax * np.power((1+ shape * np.exp(1+ shape) * np.exp(mu / ymax * np.power(1+ shape, 1+ 1/shape) * (t_lag - t))), -1/shape)) + y0

def baranyi(t, y0, t_lag, mu, ymax):
    y0 = 0   # due to the imposed preprocessing, y0==0 always.
    # rewritten with biologial parameters by PERNI et al, 2005 (doi 10.1016/j.fm.2004.11.014).
    A = t + 1/mu *np.log(np.exp(-mu *t) + np.exp(-t_lag *mu) - np.exp(-mu*t -t_lag*mu))
    return y0 + mu*A -np.log(1 + (np.exp(mu*A) -1) / np.exp(ymax - y0))

def baranyi_nolag(t, y0, mu, ymax):
    y0 = 0   # due to the imposed preprocessing, y0==0 always.
    # So it's a 'baranyi' with 't_lag'==0. This means that 'A' == 't'.
    return y0 + mu*t -np.log(1 + (np.exp(mu*t) -1) / np.exp(ymax - y0))

def baranyi_nostat(t, y0, t_lag, mu):
    y0 = 0   # due to the imposed preprocessing, y0==0 always.
    # So it's a 'baranyi' with 'ymax'==+inf. 
    A = t + 1/mu *np.log(np.exp(-mu *t) + np.exp(-t_lag *mu) - np.exp(-mu*t -t_lag*mu))
    return y0 + mu*A 




def R2(y_true, y_pred):
    RSS = np.sum((y_true - y_pred)**2)  # residual sum of squares
    TSS = np.sum((y_true - np.mean(y_true))**2) # total sum of squares
    r2 = 1 - (RSS / TSS)
    return round(r2, 2)

def AIC(y_true, y_pred, n_params):
    # taken from Lopez et al, 2004 (doi 10.1016/j.ijfoodmicro.2004.03.026)
    RSS = np.sum((y_true - y_pred)**2)  # residual sum of squares
    n_points = len(y_true)  # assuming len(y_true)==len(y_pred)
    aic = n_points * np.exp(RSS/n_points) + 2*(n_params+1) + 2*(n_params+1)*(n_params+2)/(n_points-n_params-2)
    return round(aic, 2)




def get_more_t_point(time, mult=10):
    # eg: draw fitted curve with 3 times more points
    time_mult = []
    for i in time[:-1]:  # exclude last time point
        for j in range(mult):
            time_mult.append(i + (time[i+1]-time[i])/mult*j)
    time_mult.append(time[-1])
    return np.array(time_mult)




def guess_params(time, od, n_bins=7):
    
    # STEP 1: create bins
    step = (max(od) - min(od))/ (n_bins-1)
    bins = {}  # alwys n_bins + 1
    for i in range(n_bins):
        bin_start = min(od) + step*i - step/2
        bin_end = bin_start + step
        bins[(bin_start, bin_end)] = []

    # STEP 2: populate bins 
    for i, odi in enumerate(od): 
        for (bin_start, bin_end) in bins.keys():
            if odi > bin_start and odi <= bin_end:
                bins[(bin_start, bin_end)].append((time[i], odi))

    # STEP 3: guess values 
    key_lag = list(bins.keys())[0]
    key_plateau = list(bins.keys())[-1]
    guess_t_lag = max([ti for ti, odi in bins[key_lag]])
    guess_od_lag = statistics.mean([odi for ti, odi in bins[key_lag]])
    guess_t_max = min([ti for ti, odi in bins[key_plateau]])
    guess_t_death = max([ti for ti, odi in bins[key_plateau]])
    guess_od_max = statistics.mean([odi for ti, odi in bins[key_plateau]])
    
    return guess_t_lag, guess_od_lag, guess_t_max, guess_t_death, guess_od_max


