"""Data loading utilities."""

from datetime import date
from typing import List, Optional, Union


def load(
    symbol: Union[str, List[str]],
    start: Optional[date] = None,
    end: Optional[date] = None,
    interval: str = "1d",
) -> dict:
    """
    Load historical data for the given symbol(s).

    Args:
        symbol: Stock symbol or list of symbols
        start: Start date
        end: End date
        interval: Data interval (1d, 1h, 5m, etc.)

    Returns:
        Dictionary with price data (placeholder for now)
    """
    # Handle single symbol
    if isinstance(symbol, str):
        symbols = [symbol]
    else:
        symbols = symbol

    # Default dates
    if end is None:
        end = date.today()
    if start is None:
        start = date(end.year - 1, end.month, end.day)

    print("📊 Loading data...")
    print(f"   Symbols: {', '.join(symbols)}")
    print(f"   Period: {start} to {end}")
    print(f"   Interval: {interval}")
    print("\n   (Yahoo Finance integration coming soon!)")

    # Return placeholder data
    return {
        "symbols": symbols,
        "start": start,
        "end": end,
        "interval": interval,
        "data": None,  # Will be pandas DataFrame
    }
