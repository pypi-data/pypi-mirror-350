def calc(
    price: float,
    fwd: float,
    strike: float,
    exp: float,
    df: float,
    is_call: bool,
    tol: float = 1e-8,
    max_iter: int = 10,
) -> float:
    """
    Calculate the implied volatility using the Newton-Raphson method.

    Args:
        price (float): The market price of the option.
        fwd (float): The forward price of the underlying asset.
        strike (float): The strike price of the option.
        exp (float): The time to expiration in years.
        df (float): The discount factor.
        is_call (bool): True for call options, False for put options.
        tol (float, optional): Tolerance for convergence. Default is 1e-8.
        max_iter (int, optional): Maximum number of iterations. Default is 10.

    Returns:
        float: The implied volatility.
    """

def bs(
    fwd: float,
    strike: float,
    exp_t: float,
    df: float,
    vol: float,
    is_call: bool,
) -> float:
    """
    Black-Scholes formula for European options.

    Args:
        fwd (float): The forward price of the underlying asset.
        strike (float): The strike price of the option.
        exp_t (float): The time to expiration in years.
        df (float): The discount factor.
        vol (float): The volatility of the underlying asset.
        is_call (bool): True for call options, False for put options.

    Returns:
        float: The option price.
    """
