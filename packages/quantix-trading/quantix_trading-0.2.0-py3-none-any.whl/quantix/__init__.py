"""Quantix - Fast and intuitive backtesting for Python."""

__version__ = "0.2.0"

# Core imports - will be implemented soon
from quantix.core.backtest import backtest

# Convenience imports
from quantix.core.signals import buy, hold, sell
from quantix.core.strategy import strategy
from quantix.data.loader import load

__all__ = ["strategy", "backtest", "load", "buy", "sell", "hold"]

# ASCII art for fun
_LOGO = r"""
  ____                    _   _
 / __ \                  | | (_)
| |  | |_   _  __ _ _ __ | |_ ___  __
| |  | | | | |/ _` | '_ \| __| \ \/ /
| |__| | |_| | (_| | | | | |_| |>  <
 \___\_\\__,_|\__,_|_| |_|\__|_/_/\_\

Fast and intuitive backtesting for Python
"""


def _print_logo():
    print(_LOGO)
