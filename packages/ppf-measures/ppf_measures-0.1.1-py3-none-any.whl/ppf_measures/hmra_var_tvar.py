import numpy as np
from hmra import hmra

def simulate_var_tvar(v, D, x0, eps, eul_dt, p, r_values, n_samples, max_fail_ratio):
    """
    Compute the Value at Risk (VaR) and Tail Value at Risk (TVaR) via simulation 
    of the first-passage time (FPT) using the HMRA method.

    Parameters
    ----------
    v : float
        Drift constant.
    D : float
        Diffusion constant.
    x0 : float
        Initial position.
    eps : float
        Accuracy threshold for HMRA.
    eul_dt : float
        Time step for Euler simulation.
    p : float
        Confidence level for VaR/TVaR (e.g., 0.95).
    r_values : array_like
        Array of resetting rate values to evaluate.
    n_samples : int
        Number of simulation samples per r.
    max_fail_ratio : float
        Maximum allowed ratio of failed samples for a valid result.

    Returns
    -------
    var_values : list of float
        Value at Risk values for each r.
    tvar_values : list of float
        Tail Value at Risk values for each r.
    """

    def simulate_fpt(r):
        try:
            fpt, _, success = hmra(v, D, r, x0, eps, eul_dt)
            return fpt if success else None
        except Exception:
            return None

    var_values = []
    tvar_values = []

    for r in r_values:
        fpt_samples = [simulate_fpt(r) for _ in range(n_samples)]
        fpt_samples = [fpt for fpt in fpt_samples if fpt is not None]

        fail_ratio = 1 - len(fpt_samples) / n_samples
        if fail_ratio > max_fail_ratio:
            print(f"[WARNING] Skipping r = {r:.6f}: {fail_ratio:.2%} failed.")
            var_values.append(np.nan)
            tvar_values.append(np.nan)
            continue

        fpt_array = np.array(fpt_samples)
        var = np.quantile(fpt_array, p)
        var_values.append(var)

        tail_samples = fpt_array[fpt_array >= var]
        tvar = np.mean(tail_samples) if len(tail_samples) > 0 else np.nan
        tvar_values.append(tvar)

    return var_values, tvar_values
