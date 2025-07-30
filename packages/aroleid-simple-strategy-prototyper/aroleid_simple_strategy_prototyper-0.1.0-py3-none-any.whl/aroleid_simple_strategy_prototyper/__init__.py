"""
Aroleid Simple Strategy Prototyper

A Python package for backtesting trading strategies with OHLCV data.
"""

__version__ = "0.1.0"

# Import main classes and enums from backtester module
from .backtester import (
    Backtester,
    RecordType,
    OrderType,
    Side,
    OrderBase,
    MarketOrder,
    LimitOrder,
    StopOrder,
)

# Import utility functions from data_converter module
from .helpers import convert_csv_to_databento_format

# Define what gets exported when using "from aroleid_simple_strategy_prototyper import *"
__all__ = [
    # Main backtesting class
    "Backtester",
    # Enums
    "RecordType",
    "OrderType",
    "Side",
    # Order classes
    "OrderBase",
    "MarketOrder",
    "LimitOrder",
    "StopOrder",
    # Utility functions
    "convert_csv_to_databento_format",
    # Package metadata
    "__version__",
]
