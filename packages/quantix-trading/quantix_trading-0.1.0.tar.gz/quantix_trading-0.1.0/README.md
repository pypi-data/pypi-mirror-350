# Quantix

Fast and intuitive backtesting for Python.

## Coming Soon!

```python
import quantix as qx

@qx.strategy
def momentum(bar):
    if bar.rsi < 30:
        return 'buy'
        
result = qx.backtest('AAPL', momentum)