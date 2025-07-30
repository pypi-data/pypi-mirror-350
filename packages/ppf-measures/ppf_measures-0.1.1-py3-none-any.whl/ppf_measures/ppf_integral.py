import numpy as np
import mpmath as mp
import scipy as sp
import warnings
import ppf_approx.lt_fptd as lt_fptd
import ppf_approx.mfpt as mfpt

def integral_ppf(m_ord, n_ord, v, D, x0, r, tval, correction = True):
    """
    Perform the Pade-partial fraction approximation to invert a Laplace transform of the bounded and biased Brownian trajectory with stochastic resetting

    Parameters
    ----------
    m_ord : Integer
        Numerator order of the Pade approximation.
    n_ord : Integer
        Denominator order of the Pade approximation.
    v : Float
        Drift constant.
    D : Float
        Diffusion constant.
    x0 : Float
        Initial position. Must be from 0 <= x0 < 1.
    r : Float
        Resetting rate.
    tval : Array
        Range of time values at which the PPF will be performed. Single values are accepted.
    correction : Boolean, optional
        Determines whether the PPF will perform the correction steps or not. The default is True.

    Returns
    -------
    Array
        PPF-inverted FPT distribution.

    """
    #STEP 1: Pade Approximation
    #Compute for the m+n-th Taylor approximants
    lt_fpt = lambda s: lt_fptd(v, D, -s, x0, r)
    g = np.array([float(mp.diff(lt_fpt, 0, i)/mp.fac(i)) for i in range(m_ord+n_ord+1)])
    
    #Solve for the numerator and denominator coefficients of the Pade approximation
    M = np.zeros((n_ord, n_ord))
    minus_m = []
    
    for ind1, i in enumerate(np.arange(m_ord+1, m_ord+n_ord+1)):
        j_bot = max(0, i-n_ord)
        
        row = np.zeros(n_ord)
        for ind2, j in enumerate(np.arange(j_bot, i+1)):
            if ind2 == 0:
                minus_m.append(g[j])
            else:
                row[ind2-1] = g[j]
        
        M[ind1] = row
        
    minus_m = -np.array(minus_m).T
    
    bud = np.linalg.solve(M , minus_m)
    #Denominator coefficients
    b = np.ones(n_ord+1)
    b[:n_ord] = np.flip(bud)
    #Numerator coefficients
    a = np.ones(m_ord+1)
    for i in range(m_ord+1):
        a[i] = np.sum([g[i-j]*b[j] for j in np.arange(0,i+1)])
    
    #STEP 2: Partial fraction decomposition
    #Partial fraction decomposition performed via residue theorem
    gammaj, alphaj, coeffj = sp.signal.residue(np.flip(a), np.flip(b))
    
    rt_checker = sp.signal.unique_roots(alphaj)
    alphaj2 = np.repeat(rt_checker[0], rt_checker[1])
    facterm = np.concatenate([np.arange(1,i+1) for i in rt_checker[1]])
    
    #STEP 3: Inversion
    def inversion(t):
        val = -(gammaj/sp.special.factorial(facterm)) * (t**(facterm-1)) * np.exp(-alphaj2 * t)
        return np.real(np.sum(val))
    
    inversion_vec = np.vectorize(inversion)
    
    #STEP 4: Corrections
    if correction:
        ana_mfpt = mfpt(v, D, x0, r)
        
        #Correction 1: Recentering to the analytical mean
        app_mfpt = sp.integrate.quad(lambda t: t*inversion(t), 0, np.inf)[0]
        tval_centered = tval-np.abs(ana_mfpt-app_mfpt)
        fpt_appr = inversion_vec(tval_centered)
    
        #Correction 2: Truncation to nonnegaative values
        fpt_appr = fpt_appr.clip(min = 0)
        
        #Correction 3: Smoothing near the origin/removal of erratic modes
        def diff_inversion(t):
            val = -(gammaj/sp.special.factorial(facterm)) * (t**(facterm-1)) * np.exp(-alphaj2 * t) * ((facterm-1)/t-alphaj2)
            return np.real(np.sum(val))
        
        def diff2_inversion(t):
            val = -(gammaj/sp.special.factorial(facterm)) * (t**(facterm-1)) * np.exp(-alphaj2 * t) * ((((facterm-1)/(t**2))*(facterm-2-(2*alphaj2*t))) + alphaj2**2)
            return np.real(np.sum(val))
        
        def modrootfinder(tg):
            root = sp.optimize.fsolve(lambda t: diff_inversion(t), tg)[0]
            check = np.isclose(diff_inversion(root), 0)
            if check:
                return root
            else:
                raise ValueError("scipy.optimize.fsolve returned a false positive result")
        
        warnings.filterwarnings("error")
        rootvals = []
        for tg in np.linspace(0, ana_mfpt, 100):
            try:
                rootvals.append(modrootfinder(tg))
            except:
                pass
        warnings.resetwarnings()
        
        unique_roots, root_count = np.unique(np.array(rootvals).round(decimals=4), return_counts = True)
        diff2_inversion_vec = np.vectorize(diff2_inversion)
        secdv = diff2_inversion_vec(unique_roots)
        
        mode_idx = np.argmax(root_count)
        is_mode_max = (secdv[mode_idx] < 0)
        
        if is_mode_max and len(unique_roots) > 1:
            fpt_appr[np.where(tval < unique_roots[mode_idx-1])] = 0
        
        #Correction 4: Renormalization
        fpt_appr /= sp.integrate.quad(inversion, 0, np.inf)[0] 
    
    else:   
        fpt_appr = inversion_vec(tval)
    
    # Compute the cumulative sum as an approximation of the integral
    integral_fpt_appr = np.cumsum(fpt_appr) * np.diff(tval, prepend=0)

    # Normalize to ensure it doesn't exceed 1
  
    integral_fpt_appr /= integral_fpt_appr[-1]


    return integral_fpt_appr



