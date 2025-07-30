import numpy as np
from ppf_integral import integral_ppf
from ppf_measures import ppf
from scipy.interpolate import interp1d


def value_at_risk(m_ord, n_ord, v, D, x0, r, tval, p, tol=1e-12, maxiter=500):
    """
    Compute the Value at Risk (VaR) using the Newton-Raphson method.

    Parameters
    ----------
    m_ord, n_ord : Integer
        Orders of the Pade approximation.
    v : Float
        Drift constant.
    D : Float
        Diffusion constant.
    x0 : Float
        Initial position. Must be from 0 <= x0 < 1.
    r : Float
        Resetting rate.
    tval : Array
        Range of time values for evaluation.
    p : Float
        The probability threshold for VaR (e.g., 0.95 for 95% VaR).
    tol : Float, optional
        The tolerance for convergence. Default is 1e-6.
    maxiter : Integer, optional
        The maximum number of iterations for Newton-Raphson. Default is 100.

    Returns
    -------
    Float
        The Value at Risk (VaR) corresponding to the probability `p`.
    """
    # Compute the CDF using integral_ppf
    integral_cdf = integral_ppf(m_ord, n_ord, v, D, x0, r, tval)
    
    # Compute the PDF using ppf (which is the derivative of the CDF)
    pdf_vals = ppf(m_ord, n_ord, v, D, x0, r, tval)
    
    # Interpolate both CDF and PDF for continuous functions
    cdf_func = interp1d(tval, integral_cdf, kind='linear', fill_value='extrapolate')
    pdf_func = interp1d(tval, pdf_vals, kind='linear', fill_value='extrapolate')

    # Define Newton-Raphson function: F(x) - p = 0
    def f(x):
        return cdf_func(x) - p

    # Derivative (already computed as ppf)
    def df(x):
        return pdf_func(x)

    # Initial guess: Median of tval
    guess = np.median(tval)

    # Newton-Raphson iteration
    for _ in range(maxiter):
        f_val = f(guess)
        df_val = df(guess)

        if abs(f_val) < tol:
            return guess  # Converged

        if df_val == 0:
            raise ValueError("Derivative is zero, Newton-Raphson method fails.")

        guess -= f_val / df_val  # Newton-Raphson update

    raise ValueError("Newton-Raphson did not converge within max iterations.")
