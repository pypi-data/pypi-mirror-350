import abc
import dataclasses
import enum
import logging
import pandas as pd
import uuid

pd.set_option("display.width", 1000)
pd.set_option("display.max_columns", None)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class RecordType(enum.Enum):
    OHLCV_1S = 32
    OHLCV_1M = 33
    OHLCV_1H = 34
    OHLCV_1D = 35

    @classmethod
    def to_string(cls, rtype: int) -> str:
        match rtype:
            case cls.OHLCV_1S.value:
                return "1s Bars"
            case cls.OHLCV_1M.value:
                return "1m Bars"
            case cls.OHLCV_1H.value:
                return "1h Bars"
            case cls.OHLCV_1D.value:
                return "1d Bars"
            case _:
                return f"Unknown ({rtype})"


class OrderType(enum.Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"


class Side(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclasses.dataclass
class OrderBase:
    order_id: uuid.UUID
    ts_event: pd.Timestamp
    order_direction: Side
    quantity: float


@dataclasses.dataclass
class MarketOrder(OrderBase):
    order_type: OrderType = OrderType.MARKET


@dataclasses.dataclass
class LimitOrder(OrderBase):
    limit_price: float
    order_type: OrderType = OrderType.LIMIT


@dataclasses.dataclass
class StopOrder(OrderBase):
    stop_price: float
    order_type: OrderType = OrderType.STOP


class Backtester(abc.ABC):

    def __init__(self):
        self._marketed_data_df = pd.DataFrame()
        self._orders_df = pd.DataFrame()
        self._trades_df = pd.DataFrame()

    def load_historical_market_data(
        self, path_to_dbcsv: str, symbol: str | None = None
    ) -> None:
        try:
            logger.info(f"Reading CSV file: {path_to_dbcsv}...")
            self._market_data_df = pd.read_csv(
                path_to_dbcsv,
                usecols=[
                    "ts_event",
                    "rtype",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "symbol",
                ],
                dtype={
                    "ts_event": int,
                    "rtype": int,
                    "open": int,
                    "high": int,
                    "low": int,
                    "close": int,
                    "volume": int,
                    "symbol": str,
                },
            )

            if symbol is not None:
                logger.info(f"Filtering data for symbol {symbol}...")
                self._market_data_df = self._market_data_df[
                    self._market_data_df["symbol"] == symbol
                ]

            logger.info(
                "Converting timestamps and price values to human-readable formats..."
            )
            self._market_data_df["ts_event"] = pd.to_datetime(
                self._market_data_df["ts_event"], unit="ns"
            )
            self._market_data_df["open"] = self._market_data_df["open"] / 1e9
            self._market_data_df["high"] = self._market_data_df["high"] / 1e9
            self._market_data_df["low"] = self._market_data_df["low"] / 1e9
            self._market_data_df["close"] = self._market_data_df["close"] / 1e9

            _rtypes = self._market_data_df["rtype"].unique().tolist()
            if len(_rtypes) != 1:
                raise ValueError(f"Expected single rtype but found multiple: {_rtypes}")

            logger.info(
                f"Data successfully loaded into pandas DataFrame: "
                f"{self._market_data_df['ts_event'].min()} to "
                f"{self._market_data_df['ts_event'].max()}; "
                f"Record type: {RecordType.to_string(_rtypes[0])}; "
                f"Number of bars: {len(self._market_data_df)}."
            )
            logger.debug(
                f"Inspecting pandas DataFrame with historical OHLCV data:"
                f"\n{self._market_data_df.head().to_string(index=False)}\n"
                f"...\n{self._market_data_df.tail().to_string(index=False)}"
            )

        except Exception as e:
            logger.error(f"Error loading CSV file: {str(e)}")
            self._market_data_df = pd.DataFrame()
            raise

    @abc.abstractmethod
    def add_indicators(self) -> None:
        pass

    @abc.abstractmethod
    def strategy(self, row: pd.Series) -> None:
        pass
