use errorfunctions::RealErrorFunctions;
use std::f64::consts::{FRAC_2_PI, PI, SQRT_2};

const EPSILON: f64 = f64::EPSILON;
const POLYA_FACTOR: f64 = FRAC_2_PI;

fn sqrt_eps() -> f64 {
    EPSILON.sqrt()
}

pub fn ivol_householder(
    price: f64,
    fwd: f64,
    strike: f64,
    exp_t: f64,
    df: f64,
    is_call: bool,
    tol: f64,
    n_iter: usize,
) -> f64 {
    let (norm_undisc_price, mns) = norm_price(price, fwd, strike, df, is_call);

    if norm_undisc_price >= 1.0 / mns || norm_undisc_price <= 0.0 {
        return 0.0;
    }

    let log_mns = mns.ln();
    let mut x1 = ivol_guess_undisc_call(norm_undisc_price, mns, log_mns);
    let ftol = tol.max(EPSILON) * norm_undisc_price.max(1.0);
    let log_norm_undisc_price = norm_undisc_price.ln();
    let (mut fb, mut fb_over_fpb, mut fp2b_over_fpb, mut fp3b_over_dpb) =
        obj_householder_log(log_mns, mns, x1, log_norm_undisc_price);

    if fb.abs() >= ftol {
        for _ in 0..n_iter {
            let x0 = x1;
            let hn = -fb_over_fpb;
            let num = 1.0 + fp2b_over_fpb * hn / 2.0;
            let denom = 1.0 + fp2b_over_fpb * hn + fp3b_over_dpb / 6.0 * hn * hn;
            x1 = x0 + hn * num / denom;
            let res = obj_householder_log(log_mns, mns, x1, log_norm_undisc_price);
            fb = res.0;
            fb_over_fpb = res.1;
            fp2b_over_fpb = res.2;
            fp3b_over_dpb = res.3;
            let xtol = x1.abs().max(1.0) * 32.0 * EPSILON;
            if (x1 - x0).abs() <= xtol || fb.abs() < ftol {
                break;
            }
        }
    }

    x1 / exp_t.sqrt()
}

fn norm_price(price: f64, fwd: f64, strike: f64, df: f64, is_call: bool) -> (f64, f64) {
    let norm_undisc_price = price / fwd / df;
    let fwd_mns = fwd / strike;

    match (is_call, fwd_mns > 1.0) {
        (true, false) => (norm_undisc_price, fwd_mns),
        (true, true) => (
            (fwd * (norm_undisc_price - 1.0) + strike) / strike,
            1.0 / fwd_mns,
        ),
        (false, false) => (norm_undisc_price + 1.0 - 1.0 / fwd_mns, fwd_mns),
        (false, true) => (fwd_mns * norm_undisc_price, 1.0 / fwd_mns),
    }
}

fn ivol_guess_undisc_call(price: f64, mns: f64, log_mns: f64) -> f64 {
    let alpha = price * mns;
    let em2piy = (-POLYA_FACTOR * log_mns).exp();
    let a = (mns * em2piy - 1.0 / (mns * em2piy)).powi(2);
    let r2 = (2.0 * alpha - mns + 1.0).powi(2);
    let mut b = 4.0 * (em2piy + 1.0 / em2piy)
        - 2.0 / mns * (mns * em2piy + 1.0 / (mns * em2piy)) * ((mns * mns) + 1.0 - r2);

    let beta = if alpha.abs() < sqrt_eps() {
        let c = -16.0 * (1.0 - 1.0 / mns) * alpha
            - 16.0 * (1.0 - 3.0 / mns + 1.0 / (mns * mns)) * alpha * alpha;
        c / b
    } else if (mns - alpha).abs() < sqrt_eps() {
        let c = -16.0 * (1.0 + 1.0 / mns) * (alpha - mns)
            - 16.0 * (1.0 + 3.0 / mns + 1.0 / (mns * mns)) * (alpha - mns) * (alpha - mns);
        if c == 0.0 {
            b / a
        } else {
            c / b
        }
    } else if log_mns.abs() < sqrt_eps() {
        let a2 = alpha * alpha;
        let a4 = a2 * a2;
        let c = 16.0 * ((a2 - a4) + (2.0 * a4 + 2.0 * alpha * a2 - a2 - alpha) * log_mns);
        b = 16.0 * (a2 - log_mns * (alpha + a2));
        c / b
    } else {
        let eym1 = mns - 1.0;
        let eyp1 = mns + 1.0;
        let c = 1.0 / (mns * mns) * (r2 - eym1 * eym1) * (eyp1 * eyp1 - r2);
        2.0 * c / (b + (b * b + 4.0 * a * c).sqrt())
    };

    let beta = if beta < 0.0 { sqrt_eps() } else { beta };

    let gamma = -beta.ln() / POLYA_FACTOR;

    if log_mns >= 0.0 {
        let a_sqrt_y = 0.5 * (1.0 + (1.0 - em2piy * em2piy).sqrt());
        let gmy = (gamma - log_mns).max(0.0);
        if price <= a_sqrt_y - 0.5 / mns {
            return (gamma + log_mns).sqrt() + gmy.sqrt();
        }
        return (gamma + log_mns).sqrt() + gmy.sqrt();
    }

    let a_sqrt_y = 0.5 * (1.0 - (1.0 - 1.0 / (em2piy * em2piy)).sqrt());
    let mut gpy = gamma + log_mns;
    if gpy < 0.0 {
        gpy = 0.0;
    }
    if price <= 0.5 - a_sqrt_y / mns {
        return -(gpy).sqrt() + (gamma - log_mns).sqrt();
    }
    (gpy).sqrt() + (gamma - log_mns).sqrt()
}

fn obj_householder_log(
    log_mns: f64,
    mns: f64,
    sigma_root_t: f64,
    log_norm_undisc_price: f64,
) -> (f64, f64, f64, f64) {
    let sigma_root_t = sigma_root_t.abs();
    let h = log_mns / sigma_root_t;
    let t = sigma_root_t / 2.0;
    let h2 = h * h;
    let t2 = t * t;
    let np_m_nm = (-(h + t) / SQRT_2).erfcx() - ((-(h - t)) / SQRT_2).erfcx();
    let norm = 1.0 / (2.0 * mns.sqrt()) * (-(h2 + t2) / 2.0).exp();
    let log_c_estimate_diff = (norm * np_m_nm).ln() - log_norm_undisc_price;
    let log_vega = 2.0 / (2.0 * PI).sqrt() / np_m_nm;
    let volga_over_vega = (h + t) * (h - t) / sigma_root_t;
    let log_volga_over_vega = volga_over_vega - log_vega;
    let c3_over_vega = (-3.0 * h2 - t2 + (h2 - t2).powi(2)) / (sigma_root_t * sigma_root_t);
    let log_c3_over_vega =
        c3_over_vega - 3.0 * log_vega * volga_over_vega + 2.0 * log_vega * log_vega;

    (
        log_c_estimate_diff,
        log_c_estimate_diff / log_vega,
        log_volga_over_vega,
        log_c3_over_vega,
    )
}
