from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define which ticker this strategy will apply to
        self.ticker = "AAPL"  # You can change this to any ticker of interest

    @property
    def assets(self):
        # The strategy is specifically for the stock ticker defined in __init__
        return [self.ticker]

    @property
    def interval(self):
        # Define the data interval; using daily data in this example
        return "1day"

    def run(self, data):
        # Use Exponential Moving Averages with two different lengths
        short_ema_length = 12
        long_ema_length = 26
        
        # Compute EMAs
        short_ema = EMA(self.ticker, data["ohlcv"], length=short_ema_length)
        long_ema = EMA(self.ticker, data["ohlcv"], length=long_ema_length)

        # Default allocation, no position
        ticker_allocation = 0

        if short_ema and long_ema and len(short_ema) > 0 and len(long_ema) > 0:
            # Check if the short EMA has crossed above the long EMA
            if short_ema[-1] > long_ema[-1]:
                log(f"{self.ticker}: Short EMA is above Long EMA, indicating a potential uptrend.")
                ticker_allocation = 1  # Allocate fully to this ticker
            else:
                log(f"{self.ticker}: Short EMA is below Long EMA, indicating no position.")

        # Return the allocation as a TargetAllocation object
        return TargetAllocation({self.ticker: ticker_allocation})