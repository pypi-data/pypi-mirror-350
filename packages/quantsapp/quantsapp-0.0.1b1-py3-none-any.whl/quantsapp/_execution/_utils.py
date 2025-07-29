# Built-in Modules
import datetime as dt

# ----------------------------------------------------------------------------------------------------

def convert_update_sec_to_datetime(micro_sec_value: int, tz: dt.timezone = dt.UTC) -> dt.datetime:

    return dt.datetime.fromtimestamp(
        timestamp=micro_sec_value/1e6,  # Convert microsecond to second
        tz=tz,
    )