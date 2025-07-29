import time

import ivol

start = time.time()


mns = [
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    0.92,
    0.94,
    0.95,
    0.96,
    0.97,
    0.98,
    0.99,
    1.0,
    1.01,
    1.02,
    1.03,
    1.04,
    1.05,
    1.06,
    1.08,
    1.09,
    1.1,
    1.2,
    1.3,
    1.4,
    1.5,
    1.6,
    1.7,
    1.8,
    1.9,
]
exps = [0.25, 0.5, 0.75, 1.0, 2.0, 3.0]
is_calls = [True, False]
num_times = 1

# strike = 100.0
# fwd = 0.96 * strike
# exp = 0.75
# iv = 0.2
# is_call = True
# px = ivol.bs(fwd, strike, 0.75, 1.0, iv, is_call)


def bs(mns: float, exp: float, vol: float, is_call: float):
    import numpy as np
    from scipy.stats import norm

    strike = 100.0
    fwd = mns * strike
    vol_root_t = vol * np.sqrt(exp)
    d1 = np.log(mns) / vol_root_t + vol_root_t / 2
    d2 = d1 - vol_root_t
    phi = 1.0 if is_call else -1.0
    nd1 = norm.cdf(phi * d1)
    nd2 = norm.cdf(phi * d2)
    return phi * (fwd * nd1 - strike * nd2)


tol = 1e-12
iv = 0.2
num_wrong = 0
for _ in range(num_times):
    for is_call in is_calls:
        for exp in exps:
            for mn in mns:
                fwd = 100.0 * mn
                # px = ivol.bs(fwd, 100.0, exp, 1.0, iv, is_call)
                px = bs(mn, exp, iv, is_call)
                vol = ivol.calc(px, fwd, 100.0, exp, 1.0, is_call, tol, 30)
                px_implied = bs(mn, exp, vol, is_call)
                if (err := abs(vol - iv)) > tol:
                    # if (err := abs(px_implied - px) / fwd) > tol:
                    num_wrong += 1
                    print(f"implied vol error greater than {tol}, error: {err}")
                    # print(f"implied vol error greater than {tol}, implied vol: {err}")
                    # print(f"price error greater than {tol}, error: {err}")
                    print(f"{'call' if is_call else 'put'}, {exp}, {mn}")

end = time.time()
num_calls = len(mns) * len(exps) * len(is_calls) * num_times
print(f"num wrong: {num_wrong}")
print(f"done {num_calls} calls in {end - start:.2f} seconds")
