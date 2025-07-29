# Built-in Modules
import typing
import datetime as dt


# Third-party Modules
from pydantic import (
    BaseModel,

    PositiveInt,
    PositiveFloat,

    Field,
    computed_field,
    model_validator,

    StrictStr,
)


# Local Modules
from quantsapp import (
    _enums as generic_enums,
    constants as generic_constants,
)
from quantsapp.exceptions import InvalidInputError


# -- Typed Dicts -------------------------------------------------------------------------------------


NumericString_Type = typing.NewType('NumericString_Type', str)
"""sample:-
```
'1'
'1.1'
"""


DateTime_Type = typing.NewType('DateTime_Type', str)
"""sample:-
```
'02-May-25 23:59:59'
"""


DateTimeIso_Type = typing.NewType('DateTimeIso_Type', str)
"""sample:-
```
'2025-05-10T00:18:45.951177+05:30'
"""


InstrumentString_Type = typing.NewType('InstrumentString_Type', str)
"""sample:-
```
'NIFTY:26-Jun-25:c:26500'
'NIFTY:26-Jun-25:p:26500'
'NIFTY:26-Jun-25:x'
'NIFTY:26-Jun-25'  # Default is future
'NIFTY'  # Default rolling future expiry
"""


ApiResponseStatus_Type = typing.Literal['0', '1']


Exchange_Type = typing.Literal[
    'NSE-FO',
]


Country_Type = typing.Literal[
    'in',
]

AccountType_Type = typing.Literal[
    'free',
    'pro',
    'pro_plus',
]



class ApiResponseMasterData_Type(typing.TypedDict):
    """sample
    ```
    {
        'master_data': 'Base64 Gzipped Pickle data',
        'last_updated_on':'2025-05-13T06:50:06.106209+05:30',
        'pickle_protocol': PICKLE_PROTOCOL,
        'master_version': '14-May-25'
    }
    """
    master_data: str
    last_update_on: str
    pickle_protocol: int
    master_version: str


class MasterExpiryData_Type(typing.TypedDict):
    """sample
    ```
    {
        "weekly": [
            "09112023"  # Instead of expiry in string it will be in datatime
        ],
        "all": [
            "09112023"
        ],
        "monthly": [
            "30112023"
        ]
    }
    """
    weekly: list[dt.datetime]
    all: list[dt.datetime]
    monthly: list[dt.datetime]

class MasterSymbolData_Type(typing.TypedDict):
    """sample
    ```
    {
        "lot_size": {
            datetime.datetime(2025, 5, 29, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800), 'IST')): 50,
        },
        "expiry": MasterExpiryData_Type,
        "strikes": {
            "07122023": [
                "16150"
            ]
        }
    }
    """
    lot_size: dict[dt.datetime, int]
    expiry: MasterExpiryData_Type
    strikes: dict[dt.datetime, list[int | float]]


class MasterScripData_Type(typing.TypedDict):
    """sample
    ```
    {
        "instruments_to_scrip": {
            "NIFTY:25012024|x": "55319"
        },
        "scrip_to_instruments": {
            "55319": "NIFTY:25012024|x"
        }
    }
    """
    instruments_to_scrip: dict[str, NumericString_Type]
    scrip_to_instruments: dict[NumericString_Type, str]


class MasterData_Type(typing.TypedDict):
    """sample
    ```
    {
        "symbol_data": {
            'NIFTY': MasterSymbolData_Type,
        },
        "scrip_data": MasterScripData_Type
    }
    """
    symbol_data: dict[str, MasterSymbolData_Type]
    scrip_data: MasterScripData_Type





# -- Pydantic Models ---------------------------------------------------------------------------------



class Response_Error(BaseModel):
    code: typing.Optional[generic_enums.ErrorCodes] = Field(default=None)
    msg: typing.Optional[str] = Field(default=None)

class _BaseResponse(BaseModel):
    success: bool
    error: typing.Optional[Response_Error] = Field(default_factory=Response_Error)



class AccountDetails_Pydantic(BaseModel, frozen=True):
    API_KEY: str
    USER_ID: str


class _InternalSessionData_Type(typing.TypedDict):
    qapp_ac_data: AccountDetails_Pydantic


class _Instrument_Pydantic(BaseModel):

    # Variables
    symbol: StrictStr
    expiry: typing.Optional[dt.datetime] = Field(default=None)
    instrument_type: typing.Optional[generic_enums.InstrumentType] = Field(default=generic_enums.InstrumentType.FUTURE)
    strike: typing.Optional[PositiveInt | PositiveFloat] = Field(
        default=None,
        gt=0,
        validate_default=True,
    )

    # ---------------------------------------------------------------------------

    @model_validator(mode='after')
    def validate_instr(self: typing.Self) -> typing.Self:

        from quantsapp._master_data import MasterData

        # Validation - Symbol
        if not MasterData.is_valid_symbol(self.symbol):
            raise InvalidInputError(f"Invalid symbol = {self.symbol}")

        # Make the model mutable to set default values
        self.model_config['frozen'] = False

        # If expiry not set, then consider rolling future expiry instrument
        if not self.expiry:
            self.expiry = MasterData.master_data['symbol_data'][self.symbol]['expiry']['monthly'][0]
            self.instrument_type = generic_enums.InstrumentType.FUTURE
            self.strike = None

        else:
            # Validation - Expiry
            self.expiry = self.expiry.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=generic_constants.DT_ZONE_IST,
            )
            if not MasterData.is_valid_expiry(symbol=self.symbol, expiry=self.expiry):
                raise InvalidInputError(f"Invalid Expiry for symbol ({self.symbol}) = {self.expiry:%d-%b-%Y}. Available expiries are {[f'{_exp:%d-%b-%Y}' for _exp in MasterData.get_all_expiries(self.symbol)]}")

            # If instrument_type not set, then consider future instrument of that expiry
            if not self.instrument_type:
                self.instrument_type = generic_enums.InstrumentType.FUTURE
                self.strike = None

            else:
                # Validation - Strike
                if self.instrument_type != generic_enums.InstrumentType.FUTURE:
                    if not MasterData.is_valid_strike(symbol=self.symbol, expiry=self.expiry, strike=self.strike):
                        raise InvalidInputError(f"Invalid Strike for symbol ({self.symbol}), Expiry ({self.expiry:%d-%b-%Y}) = {self.strike}. Available strikes are {MasterData.get_all_strikes(self.symbol, self.expiry)}")

        # To avoid modifying the values once all set, make it immutable
        self.model_config['frozen'] = True
        # TODO remove it later
        # self.__class__.model_config = ConfigDict(
        #     frozen=True,
        # )

        return self

    # ---------------------------------------------------------------------------

    @classmethod
    def from_api_str(cls, instr: str) -> typing.Self:
        """Convert API String representation of instr to Instance Model
            'NIFTY:15-May-25:x'
            'NIFTY:15-May-25:c:25200'
        """

        from quantsapp import _config as generic_config
        from quantsapp import _utils as generic_utils

        _tmp = generic_config.re_api_instr.search(instr).groupdict()

        _instr_data: dict[str, typing.Any] = {
            'symbol': _tmp['symbol'],
            'expiry': None,
            'instrument_type': None,
            'strike': None,
        }

        if _tmp['expiry']:
            _instr_data['expiry'] = dt.datetime.strptime(_tmp['expiry'], generic_config.EXPIRY_FORMAT)

            if _tmp['instrument_type']:
                _instr_data['instrument_type'] = generic_enums.InstrumentType(_tmp['instrument_type'].lower())

                if _tmp['strike']:
                    _instr_data['strike'] = generic_utils.get_int_or_float(_tmp['strike']) if _tmp['strike'] else None

        return cls(**_instr_data)

    # ---------------------------------------------------------------------------

    @computed_field
    @property
    def api_instr_str(self) -> str:
        """String representation to be used on API level conversions
            'NIFTY:15-May-25:x'
            'NIFTY:15-May-25:c:25200'
        """

        _instr = self.symbol

        _instr += f":{self.expiry:%d-%b-%y}"

        if self.instrument_type == generic_enums.InstrumentType.FUTURE:
            _instr += ':x'
        else:
            _instr += f":{self.instrument_type.value.lower()}:{self.strike}"

        return _instr


    # ---------------------------------------------------------------------------

    @computed_field
    @property
    def api_expiry_str(self) -> str:
        """String representation of expiry to be used on API level conversions
            '%d-%b-%y' - '15-May-25'
        """
        from quantsapp._execution import _config as execution_config

        return self.expiry.strftime(execution_config.BROKER_ORDER_PLACEMENT_DATE_FORMAT)