"""Backtesting engine."""

import warnings
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class BacktestResult:
    """Results from a backtest."""

    total_return: float = 0.15
    sharpe_ratio: float = 1.2
    max_drawdown: float = -0.08
    win_rate: float = 0.55

    def plot(self):
        """Plot backtest results."""
        print("📈 Plotting results...")
        print(f"   Total Return: {self.total_return:.2%}")
        print(f"   Sharpe Ratio: {self.sharpe_ratio:.2f}")
        print(f"   Max Drawdown: {self.max_drawdown:.2%}")
        print(f"   Win Rate: {self.win_rate:.2%}")
        print("\n   (Interactive plots coming soon!)")

    def summary(self) -> str:
        """Return a summary of results."""
        return (
            f"Total Return: {self.total_return:.2%}\n"
            f"Sharpe Ratio: {self.sharpe_ratio:.2f}\n"
            f"Max Drawdown: {self.max_drawdown:.2%}\n"
            f"Win Rate: {self.win_rate:.2%}"
        )


def backtest(
    data: Any, strategy: Callable, cash: float = 10000, commission: float = 0.001
) -> BacktestResult:
    """
    Run a backtest with the given strategy and data.

    Args:
        data: Historical price data
        strategy: Trading strategy function
        cash: Starting cash
        commission: Commission per trade

    Returns:
        BacktestResult object
    """
    # Check if strategy is decorated
    if not hasattr(strategy, "_is_strategy"):
        warnings.warn(
            "Strategy function should be decorated with @qx.strategy",
            UserWarning,
            stacklevel=2,
        )

    print("🚀 Running backtest...")
    print(f"   Strategy: {strategy.__name__}")
    print(f"   Starting Cash: ${cash:,.2f}")
    print(f"   Commission: {commission:.3%}")
    print("\n   (Full backtesting engine coming soon!)")

    # Return placeholder results
    return BacktestResult()
