import pandas as pd
import numpy as np

def stat(model, obs, min=None, max=None, digit = 6):
    """
    Calculate model performance statistics.

    Parameters:
    - model (array-like): Model predictions
    - obs (array-like): Observed values

    Returns:
    - DataFrame: Contains n, Obs, Sim, r, IOA, FA2, RMSE, MB, ME, NMB (%), NME (%)
    
    Created on Thu Jul 17 1:44:00 2025
    @author: D. Schuch
    """
    m = np.array(model)
    o = np.array(obs)
    
    if len(m) != len(o):
        raise ValueError("Model and Observation arrays must have the same length.")

    valid = np.ones_like(o, dtype=bool)
    if min is not None:
        print(f"Filtering out observations below {min}")
        valid &= o >= min
    if max is not None:
        print(f"Filtering out observations above {max}")
        valid &= o <= max

    m = m[valid]
    o = o[valid]

    n = len(o)                                       # Number of pairs
    obs_mean = np.mean(o)                            # Obs average
    sim_mean = np.mean(m)                            # model average
                                                     # Pearson correlation
    r = np.nan if np.std(m) == 0 or np.std(o) == 0 else np.corrcoef(m, o)[0, 1]     
                                                     # Index of Agreement (Willmott 1981)
    ioa = 1 - (np.sum((m - o)**2) / np.sum((np.abs(m - obs_mean) + np.abs(o - obs_mean))**2))
                                                     # Factor of 2
    fa2 = np.mean(((m[o != 0] / o[o != 0]) < 2) & ((m[o != 0] / o[o != 0]) > 0.5)) 
    rmse = np.sqrt(np.mean((m - o)**2))              # RMSE
    mb = np.mean(m - o)                              # Mean Bias
    me = np.mean(np.abs(m - o))                      # Mean Error (Mean Absolute Error)
    nmb = (np.sum(m - o) / np.sum(o)) * 100          # Normalized Mean Bias (%)
    nme = (np.sum(np.abs(m - o)) / np.sum(o)) * 100  # Normalized Mean Error (%)

    results = pd.DataFrame([{
        "n": n,
        "Obs": obs_mean,
        "Sim": sim_mean,
        "r": r,
        "IOA": ioa,
        "FA2": fa2,
        "RMSE": rmse,
        "MB": mb,
        "ME": me,
        "NMB (%)": nmb,
        "NME (%)": nme
    }])

    return results.round(digit)
