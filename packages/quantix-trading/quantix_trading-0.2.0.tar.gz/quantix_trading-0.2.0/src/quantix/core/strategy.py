"""Strategy decorator and utilities."""

from functools import wraps
from typing import Callable, Optional


def strategy(
    func: Optional[Callable] = None,
    *,
    stop_loss: Optional[float] = None,
    take_profit: Optional[float] = None,
    commission: float = 0.001,
) -> Callable:
    """
    Decorator for defining trading strategies.

    Args:
        func: The strategy function
        stop_loss: Stop loss percentage (0.02 = 2%)
        take_profit: Take profit percentage (0.05 = 5%)
        commission: Commission per trade

    Returns:
        Decorated strategy function
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        # Attach metadata
        wrapper._is_strategy = True
        wrapper._stop_loss = stop_loss
        wrapper._take_profit = take_profit
        wrapper._commission = commission

        return wrapper

    if func is None:
        return decorator
    return decorator(func)
