use pyo3::prelude::*;
use statrs::distribution::{ContinuousCDF, Normal};

pub mod householder;

/// Calculates implied volatility using the Householder method.
#[pyfunction]
#[pyo3(signature = (price, fwd, strike, exp_t, df, is_call, tol=None, n_iter=None))]
fn calc(
    price: f64,
    fwd: f64,
    strike: f64,
    exp_t: f64,
    df: f64,
    is_call: bool,
    tol: Option<f64>,
    n_iter: Option<usize>,
) -> PyResult<f64> {
    Ok(householder::ivol_householder(
        price,
        fwd,
        strike,
        exp_t,
        df,
        is_call,
        tol.unwrap_or(1e-8),
        n_iter.unwrap_or(10),
    ))
}

/// Calculates the Black-Scholes price of a call or put option.
#[pyfunction]
fn bs(fwd: f64, strike: f64, exp_t: f64, df: f64, vol: f64, is_call: bool) -> PyResult<f64> {
    let vol_root_t = vol * exp_t.sqrt();
    let d1 = f64::ln(fwd / strike) / vol_root_t + 0.5 * vol_root_t;
    let d2 = d1 - vol_root_t;
    let sgn = if is_call { 1.0 } else { -1.0 };
    let norm = Normal::standard();
    let nd1 = norm.cdf(sgn * d1);
    let nd2 = norm.cdf(sgn * d2);
    Ok(df * sgn * (fwd * nd1 - strike * nd2))
}

#[pymodule]
fn ivol(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calc, m)?)?;
    m.add_function(wrap_pyfunction!(bs, m)?)?;
    Ok(())
}
