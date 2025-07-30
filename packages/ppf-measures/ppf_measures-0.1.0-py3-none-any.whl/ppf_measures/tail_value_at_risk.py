from ppf_measures import ppf
from scipy.integrate import quad
from scipy.interpolate import interp1d
from value_at_risk import value_at_risk

def tail_value_at_risk(m_ord, n_ord, v, D, x0, r, tval, p, tol=1e-12, maxiter=500):
    """
    Compute the Tail Value at Risk (TVaR), also known as Conditional Value at Risk (CVaR).

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
        The probability threshold for VaR (e.g., 0.95 for 95% TVaR).
    tol : Float, optional
        The tolerance for convergence. Default is 1e-12.
    maxiter : Integer, optional
        The maximum number of iterations for Newton-Raphson. Default is 500.

    Returns
    -------
    Float
        The Tail Value at Risk (TVaR) corresponding to the probability `p`.
    """

    # Compute the Value at Risk (VaR)
    var_threshold = value_at_risk(m_ord, n_ord, v, D, x0, r, tval, p, tol, maxiter)

    # Compute the PDF using ppf
    pdf_vals = ppf(m_ord, n_ord, v, D, x0, r, tval)

    # Interpolate the PDF for continuous evaluation
    pdf_func = interp1d(tval, pdf_vals, kind='linear', fill_value='extrapolate')

    # Define the integrand: x * f(x) for x > VaR
    def integrand(x):
        return x * pdf_func(x)

    # Integrate from VaR to infinity (or maximum tval)
    integral_result, _ = quad(integrand, var_threshold, max(tval))

    # Compute TVaR using the formula: TVaR = (1 / (1 - p)) * Integral[ VaR to ∞ ] (x * f(x)) dx
    tvar = integral_result / (1 - p)

    return tvar
