# Built-in Modules
import enum


# Local Modules
from quantsapp._enum_meta import _QappEnumMeta

@enum.unique
class Exchange(enum.StrEnum, metaclass=_QappEnumMeta):
    NSE_FNO = 'NSE-FO'

    def __repr__(self):
        """Representation String"""
        return f"{self.__class__.__name__}.{self.name}"


@enum.unique
class Broker(enum.StrEnum, metaclass=_QappEnumMeta):
    MSTOCK = 'mstock'
    CHOICE = 'choice'
    DHAN = 'dhan'
    FIVEPAISA = 'fivepaisa'
    FIVEPAISA_XTS = 'fivepaisa-xts'
    FYERS = 'fyers'
    MOTILAL_OSWAL = 'mo'
    UPSTOX = 'upstox'
    ALICEBLUE = 'aliceblue'
    NUVAMA = 'nuvama'
    SHAREKHAN = 'sharekhan'
    ANGEL = 'angel'
    ZERODHA = 'zerodha'

    # TODO move it to metaclass
    def __repr__(self):
        """Representation String"""
        return f"{self.__class__.__name__}.{self.name}"


@enum.unique
class BrokerRole(enum.StrEnum, metaclass=_QappEnumMeta):
    OWNER = 'owner'
    READER = 'reader'
    EXECUTOR = 'executor'

    def __repr__(self):
        """Representation String"""
        return f"{self.__class__.__name__}.{self.name}"

@enum.unique
class BrokerAccountValidity(enum.StrEnum, metaclass=_QappEnumMeta):
    EXPIRED = '-2'
    UNKNOWN = '-1'
    INFINITY = '0'

    def __repr__(self):
        """Representation String"""
        return f"{self.__class__.__name__}.{self.name}"


@enum.unique
class OrderBuySell(enum.StrEnum, metaclass=_QappEnumMeta):
    BUY = 'b'
    SELL = 's'

    def __repr__(self):
        """Representation String"""
        return f"{self.__class__.__name__}.{self.name}"

@enum.unique
class OrderProductType(enum.StrEnum, metaclass=_QappEnumMeta):
    INTRADAY = 'intraday'
    NRML = 'nrml'

    def __repr__(self):
        """Representation String"""
        return f"{self.__class__.__name__}.{self.name}"


@enum.unique
class OrderType(enum.StrEnum, metaclass=_QappEnumMeta):    
    LIMIT = 'limit'
    MARKET = 'market'
    SLL = 'sll'
    SL_M = 'slm'  # TODO remove this as not being used Check with Sir

    def __repr__(self):
        """Representation String"""
        return f"{self.__class__.__name__}.{self.name}"

@enum.unique
class OrderStatus(enum.StrEnum, metaclass=_QappEnumMeta):    
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    PARTIAL = 'partial'
    PENDING = 'pending'
    FAILED = 'failed'
    PLACED = 'placed'
    REJECTED = 'rejected'
    TRANSIT = 'transit'

    def __repr__(self):
        """Representation String"""
        return f"{self.__class__.__name__}.{self.name}"


@enum.unique
class OrderValidity(enum.StrEnum, metaclass=_QappEnumMeta):    
    DAY = 'day'
    IOC = 'ioc'

    def __repr__(self):
        """Representation String"""
        return f"{self.__class__.__name__}.{self.name}"

