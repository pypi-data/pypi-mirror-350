import enum


@enum.unique
class Exchange(enum.StrEnum):
    NSE_FNO = 'NSE-FO'

    def __repr__(self):
        """Representation String"""
        return f"{self.__class__.__name__}.{self.name}"

@enum.unique
class InstrumentType(enum.StrEnum):
    CALL = 'c'
    PUT = 'p'
    FUTURE = 'x'
    __OPTIONS = 'o'  # To be used only for internal purposes

    def __repr__(self):
        """Representation String"""
        return f"{self.__class__.__name__}.{self.name}"

@enum.unique
class ErrorCodes(enum.StrEnum):

    # Input Error Codes
    INVALID_INPUT = 'QE-1'
    LOGIN_NOT_INITIATED = 'QE-2'
    TOO_MANY_REQUESTS = 'QE-3'


    # API Error Codes
    API_CONNECTION_ERROR = 'QE-API-1'
    INVALID_LOGIN_CREDENTIALS = 'QE-API-2'    
    ACCOUNT_DETAILS_NOT_FOUND = 'QE-API-3'    


    # Execution Error Codes
    NO_BROKER_ACCOUNTS_MAPPED = 'QE-EX-1'
    BROKER_LOGIN_NOT_ALLOWED = 'QE-EX-2'
    INVALID_BROKER_LOGIN_CREDENTIALS = 'QE-EX-3'
    BROKER_LOGIN_FAILED = 'QE-EX-4'
    BROKER_ACCOUNT_DELETION_FAILED = 'QE-EX-5'
    BROKER_ORDERS_LISTING_FAILED = 'QE-EX-6'
    BROKER_POSITIONS_LISTING_FAILED = 'QE-EX-7'
    BROKER_ORDERS_PLACING_FAILED = 'QE-EX-8'
    BROKER_ORDERS_CANCEL_FAILED = 'QE-EX-9'
    BROKER_ORDER_BOOK_UPDATE_FAILED = 'QE-EX-10'

    # Websocket Error Codes
    BROKER_WS_CONN_STATUS_FAILED = 'QE-EX-WS-1'
    BROKER_WS_RE_CONN_FAILED = 'QE-EX-WS-2'

    # SDK Code failure Error Code
    SDK_CODE_FAILURE = 'QE-SDK-1'