"""Trading signals."""

from typing import Any, Dict


def buy(size: float = 1.0) -> Dict[str, Any]:
    """Create a buy signal."""
    return {"action": "buy", "size": size}


def sell(size: float = 1.0) -> Dict[str, Any]:
    """Create a sell signal."""
    return {"action": "sell", "size": size}


def hold() -> Dict[str, Any]:
    """Create a hold signal."""
    return {"action": "hold", "size": 0}
