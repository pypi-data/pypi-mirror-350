# Built-in Modules
import datetime as dt



DT_ZONE_IST = dt.timezone(
    offset=dt.timedelta(
        hours=5,
        minutes=30,
    ),
    name='IST',
)