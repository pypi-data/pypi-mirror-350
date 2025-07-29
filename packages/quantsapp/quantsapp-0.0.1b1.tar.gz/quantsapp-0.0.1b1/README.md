# Quantsapp Python SDK

Python SDK for Quantsapp Order Execution

![PyPI](https://img.shields.io/pypi/v/quantsapp-dev)
<br>

<!-- ![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/5paisa/py5paisa/Publish%20package/master) -->

<!-- ![Quantsapp logo](./docs/images/quantsapp_full_logo.png) -->

<picture align="center">
  <img alt="Quantsapp Logo" src="https://s3.ap-south-1.amazonaws.com/images.quantsapp.com/webapp/assets/splash_logo.png">
</picture>


<!-- #### Documentation

Read the docs hosted [here](https://www.5paisa.com/developerapi/overview) -->

#### Features

-   Order placement, modification and cancellation
-   Fetching user info including holdings, positions, margin and order book.

-   Fetching order status and trade information.
-   Getting live orders streaming using websockets.


### Usage

#### Authentication
Get your API key & Secret key from [here](https://web.quantsapp.com/profile)
```py
import quantsapp

# Login to get session context which can be used for other modules
session_context = quantsapp.Login(
    api_key='<API_KEY>',
    secret_key='<SECRET_KEY>',
).login()
```

#### Execution Modules
```py
def broker_order_update(update):
    """This is the callback function to where the real-time broker order updates are being sent"""
    print(f"Broker Order Update received -> {update}")

# Create the Execution object
qapp_execution = quantsapp.Execution(
    session_context=session_context,
    order_updates_callback=broker_order_update,  # Optional
)
```

#### Execution Variables
All execution variables are python `enum` datatypes
```py
# Exchange enums
quantsapp.variables.Exchange
    - NSE_FNO

# Broker enums
quantsapp.variables.Broker
    - MSTOCK
    - CHOICE
    - DHAN
    - FIVEPAISA
    - FIVEPAISA_XTS
    - FYERS
    - MOTILAL_OSWAL
    - UPSTOX
    - ALICEBLUE
    - NUVAMA
    - SHAREKHAN
    - ANGEL
    - ZERODHA
quantsapp.variables.BrokerRole
    - OWNER
    - READER
    - EXECUTOR

# Order enums
quantsapp.variables.Order.ProductType
    - INTRADAY
    - NRML
quantsapp.variables.Order.Validity
    - DAY
    - IOC
quantsapp.variables.Order.OrderType
    - LIMIT
    - MARKET
    - SLL
    - SL_M
quantsapp.variables.Order.BuySell
    - BUY
    - SELL
quantsapp.variables.Order.Status
    - CANCELLED
    - COMPLETED
    - PARTIAL
    - PENDING
    - FAILED
    - PLACED
    - REJECTED
    - TRANSIT
```

#### Market Status
```py
# Get the Market Timings
qapp_market_timings = quantsapp.MarketTimings(
    exchange=qapp_execution.variables.Exchange.NSE_FNO,
)

print(f"Market opened now = {qapp_market_timings.is_market_open()}")
# Market opened now = True | False

print(f"Market Open Time = {qapp_market_timings.dt_open}")
# Market Open Time = datetime.datetime object

print(f"Market Close Time = {qapp_market_timings.dt_close = }")
# Market Open Time = datetime.datetime object
```

#### Response Model - sample
Response model which will return by all execution modules listed below
```py
response.success: bool
response.body: typing.Any  # Actual response data incase of success

# On Success
response.error: None

# On failure
response.error.code: quantsapp.ErrorCodes
response.error.msg: str
```

#### Listing Available Brokers
```py
available_brokers = qapp_execution.list_available_brokers()

if available_brokers.success:
    print(available_brokers.body)
    """sample
    {
        'access_token_login': [
            Broker.CHOICE,
            Broker.DHAN,
        ],
        'oauth_login': [
            Broker.MSTOCK,
            Broker.FIVEPAISA,
            Broker.FIVEPAISA_XTS,
            Broker.FYERS,
            Broker.ZERODHA,
            Broker.MOTILAL_OSWAL,
            Broker.UPSTOX,
            Broker.ALICEBLUE,
            Broker.NUVAMA,
        ]
    }
    """
else:
    print(f"Error on listing available brokers -> {available_brokers.error}")

if qapp_execution.variables.Broker.CHOICE in available_brokers.body['access_token_login']:
    print('CHOICE broker can be added to Quantsapp via this SDK')

if qapp_execution.variables.Broker.MSTOCK in available_brokers.body['access_token_login']:
    print("MSTOCK broker can't be added to Quantsapp via this SDK. Please add it via https://web.quantsapp.com/broker")
```

#### Listing Mapped Brokers
```py
mapped_brokers_resp = qapp_execution.list_mapped_brokers(
    resync_from_broker=False,
    from_cache=False,
)
if mapped_brokers_resp.success:
    print(mapped_brokers_resp.body)
    """sample
    {
        'brokers': {
            Broker.CHOICE: {
                '<CLIENT_ID>': {
                    'margin': {
                        Exchange.NSE_FNO: 7958.67,
                        'dt': datetime.datetime(2025, 5, 23, 13, 8, 1, tzinfo=datetime.timezone.utc)
                    },
                    'name': '<NAME>',
                    'role': BrokerRole.EXECUTOR,
                    'valid': True,
                    'validity': datetime.datetime(2025, 6, 19, 11, 57, 18, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800), 'IST'))
                }
            },
        },
        'next_margin': datetime.datetime(2025, 5, 23, 13, 23, tzinfo=datetime.timezone.utc),
        'version': 42
    }
    """
else:
    print(f"Error on getting mapped brokers -> {mapped_brokers_resp.error}")
```

#### Add Broker

> ##### DHAN
```py
add_dhan_broker_resp = qapp_execution.add_broker(
    broker=qapp_execution.variables.Broker.DHAN,
    login_credentials={
        'access_token': '<DHAN_ACCESS_TOKEN>',
    },
)
if add_dhan_broker_resp.success:
    print(f"Dhan Broker added -> {add_dhan_broker_resp.body = }")
else:
    print(f"Dhan broker failed to add -> {add_dhan_broker_resp.error}")
```

> ##### CHOICE
```py
add_choice_broker_resp = qapp_execution.add_broker(
    broker=qapp_execution.variables.Broker.CHOICE,
    login_credentials={
        'mobile': '1234567890',
        'client_access_token': '<CHOICE_ACCESS_TOKEN>',
    },
)
if add_choice_broker_resp.success:
    print(f"Choice Broker added -> {add_choice_broker_resp.body = }")
else:
    print(f"Choice broker failed to add -> {add_choice_broker_resp.error}")
```


#### Delete Broker
```py
broker_delete_resp = qapp_execution.delete_broker(
    broker=quantsapp.Broker.CHOICE,
    client_id='<CLIENT_ID>',
)
if broker_delete_resp.success:
    print(f"Broker deleted -> {broker_delete_resp.body = }")
else:
    print(f"Broker failed to delete -> {broker_delete_resp.error}")
```


#### List Orders
```py

get_orders_resp = qapp_execution.get_orderbook(
    broker=qapp_execution.variables.Broker.DHAN,
    client_id='<CLIENT_ID>',
    ascending=False,
    from_cache=True,            # Return the orders from either local cache or Quantsapp server
    resync_from_broker=False,   # Resync the orders from Broker api again

    # Optional (any combo of below filters)
    filters={
        'product': qapp_execution.variables.Order.ProductType.INTRADAY,
        'order_status': qapp_execution.variables.Order.Status.CANCELLED,
        'order_type': qapp_execution.variables.Order.OrderType.LIMIT,
        'instrument': 'NIFTY:22-May-25:p:250000',  # instrument structure = 'SYMBOL:EXPIRY:OPTION_TYPE:STRIKE'
    },
)
if get_orders_resp.success:
    print(get_orders_resp.body)
    """sample
    [
        {
            'b_orderid': '42250523454209',
            'b_usec_update': datetime.datetime(2025, 5, 23, 9, 50, 44, tzinfo=datetime.timezone.utc),
            'broker_client': BrokerClient(broker=Broker.DHAN, client_id='1100735577'),
            'buy_sell': OrderBuySell.BUY,
            'e_orderid': '1200000163510266',
            'instrument': 'NIFTY:05-Jun-25:c:25650',
            'o_ctr': 10,
            'order_status': OrderStatus.CANCELLED,
            'order_type': OrderType.LIMIT,
            'price': 1.45,
            'product_type': OrderProductType.NRML,
            'q_usec': datetime.datetime(2025, 5, 23, 9, 50, 44, tzinfo=datetime.timezone.utc),
            'qty': 75,
            'qty_filled': 0,
            'stop_price': 0.0,
            'userid': 500131
        },
    ]
    """
else:
    print(f"Error on order listing -> {get_orders_resp.error}")
```


#### Place Order
```py
place_order_resp = qapp_execution.place_order(
    broker_accounts=[
        {
            'broker': qapp_execution.variables.Broker.CHOICE,
            'client_id': '<CLIENT_ID>',
            'lot_multiplier': 1,  # Optional - Default is 1
        }
    ],
    exchange=qapp_execution.variables.Exchange.NSE_FNO,
    product=qapp_execution.variables.Order.ProductType.NRML,
    order_type=qapp_execution.variables.Order.OrderType.LIMIT,
    validity=qapp_execution.variables.Order.Validity.DAY,
    margin_benefit=True,  # Optional - Default = True
    legs=[
        {
            'qty': 75,
            'price': 0.05,
            'instrument': 'NIFTY:26-Jun-25:c:26500',
            'buy_sell': 'b',  # Buy='b', Sell='s'
            # 'stop_price': 5.4,  # Only for Stop Loss Limit Order
        },
    ],
)
if place_order_resp.success:
    print(place_order_resp.body)
else:
    print(f"Error on placing order -> {place_order_resp.error}")
```


#### Modify Order
```py
modify_order_resp = qapp_execution.modify_order(
    broker=qapp_execution.variables.Broker.CHOICE,
    client_id='<CLIENT_ID>',
    b_orderid='<BROKER_ORDER_ID>',
    e_orderid='<EXCHANGE_ORDER_ID>',
    qty=75,
    price=0.15,
)
if modify_order_resp.success:
    print(modify_order_resp.body)
else:
    print(f"Error on modifying order -> {modify_order_resp.error}")
```


#### Cancel Orders
Cancel specific orders of multiple Broker accounts
```py
cancel_orders_resp = qapp_execution.cancel_orders(
    orders_to_cancel=[
        {
            'broker': qapp_execution.variables.Broker.CHOICE,
            'client_id': '<CLIENT_ID>',
            'order_ids': [
                {
                    'b_orderid': '<BROKER_ORDER_ID>',
                    'e_orderid': '<EXCHANGE_ORDER_ID>',
                },
            ],
        },
        {
            'broker': qapp_execution.variables.Broker.DHAN,
            'client_id': '<CLIENT_ID>',
            'order_ids': [
                {
                    'b_orderid': '<BROKER_ORDER_ID>',
                    'e_orderid': '<EXCHANGE_ORDER_ID>',
                },
            ],
        },
    ],
)
if cancel_orders_resp.success:
    print('Cancel Orders:-')
    pprint(cancel_orders_resp.body)
else:
    print(f"Error on cancel order -> {cancel_orders_resp.error}")
```


#### Cancel All Orders
Cancel all orders related to specific Broker account
```py
cancel_all_orders_resp = qapp_execution.cancel_all_orders(
    broker=qapp_execution.variables.Broker.CHOICE,
    client_id='<CLIENT_ID>',
)
if cancel_all_orders_resp.success:
    print(cancel_all_orders_resp.body)
else:
    print(f"Error on cancel all orders -> {cancel_all_orders_resp.error}")
```


#### Get Positions
```py
get_positions_resp = qapp_execution.get_positions(
    broker_clients=[
        {
            'broker': qapp_execution.variables.Broker.MSTOCK,
            'client_id': '<CLIENT_ID>',
        },
        {
            'broker': qapp_execution.variables.Broker.FIVEPAISA,
            'client_id': '<CLIENT_ID>',
        },
    ],
    resync_from_broker=False,
    from_cache=True,
)
if get_positions_resp.success:
    print(get_positions_resp.body)
else:
    print(f"Error on get positions -> {get_positions_resp.error}")
```


#### Get Positions Combined
```py
get_positions_consolidated_resp = qapp_execution.get_positions_combined(
    broker_clients=[
        {
            'broker': qapp_execution.variables.Broker.MSTOCK,
            'client_id': '<CLIENT_ID>',
        },
        {
            'broker': qapp_execution.variables.Broker.CHOICE,
            'client_id': '<CLIENT_ID>',
        },
    ],
    resync_from_broker=False,
    from_cache=True,
)
if get_positions_consolidated_resp.success:
    print(get_positions_consolidated_resp.body)
else:
    print(f"Error on get consolidated positions -> {get_positions_consolidated_resp.error}")
```


#### Get Broker Websocket Status
```py
get_broker_ws_conn_status_resp = qapp_execution.get_broker_websocket_status(
    broker=qapp_execution.variables.Broker.MSTOCK,
    client_id='<CLIENT_ID>',
)
if get_broker_ws_conn_status_resp.success:
    print(get_broker_ws_conn_status_resp.body)
else:
    print(f"Error on get ws connection status -> {get_broker_ws_conn_status_resp.error}")
```


#### Broker Websocket Reconnect
```py
broker_ws_re_conn_resp = qapp_execution.broker_websocket_reconnect(
    broker=qapp_execution.variables.Broker.MSTOCK,
    client_id='<CLIENT_ID>',
)
if broker_ws_re_conn_resp.success:
    print(broker_ws_re_conn_resp.body)
else:
    print(f"Error on ws re-connection -> {broker_ws_re_conn_resp.error}")
```










<!-- 
#### Position Conversion

```py
# Convert positions
# client.position_convertion(<Exchange>,<Exchange Type>,<Scrip Name>,<Buy/Sell>,<Qty>,<From Delivery/Intraday>,<From Delivery/Intraday>)
client.position_convertion("N","C","BPCL_EQ","B",5,"D","I")
```


#### Placing an order

```py
# Note: This is an indicative order.

from py5paisa.order import Order, OrderType, Exchange

#You can pass scripdata either you can pass scripcode also.
# please use price = 0 for market Order
#use IsIntraday= true for intraday orders

#Using Scrip Data :-

#Using Scrip Code :-
client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, Price=260)
#Sample For SL order (for order to be treated as SL order just pass StopLossPrice)
client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, Price=350, IsIntraday=False, StopLossPrice=345)
#Derivative Order
client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = 57633, Qty=50, Price=1.5)

Please refer below documentation link for paramaters to be passed in cleint.place_order function
https://www.5paisa.com/developerapi/order-request-place-order

```
#### Placing offline orders (After Market Orders)

By default all orders are normal orders, pass `AHPlaced=Y` to place offline orders.

```py
client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, Price=325, AHPlaced="Y")
```

#### Modifying an order

```py
client.modify_order(ExchOrderID="1100000017861430", Qty=2,Price=261)
```

#### Cancelling an order

```py
client.cancel_order(exch_order_id="1100000017795041")
```
```py
cancel_bulk=[
            {
                "ExchOrderID": "<Exchange Order ID 1>"
            },
            {
                "ExchOrderID": "<Exchange Order ID 2>"
            },
client.cancel_bulk_order(cancel_bulk)
```

#### Order Margin Calculation

```py
client.Order_margin( Exch= "N", ExchType = "C", OrderRequestorCode = "51959929", ScripCode = "1660", PlaceModifyCancel = "P",  TransactionType = "B", AtMarket = "Y", LimitRate = 0, Volume = 5, OldTradedQty = 0, ProductType = "D", ExchOrderId = "0", CoverPositions ="N")
```
#### SquareOffAll Orders

```py
client.squareoff_all()
```
#### Bracket Order 

For placing Braket order
```py
client.bo_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, LimitPrice=330,TargetPrice=345,StopLossPrice=320,LimitPriceForSL=319,TrailingSL=1.5)

```
For placing Cover order
```py
client.cover_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, LimitPrice=330,StopLossPrice=320,TrailingSL=1.5)
```

Note:For placing Bracket order in FNO segment pass ExchType='D'

For Modifying Bracket/Cover Order only for Initial order (entry)
```py

client.modify_bo_order(ExchOrderID="1100000017861430",LimitPrice=330)
client.modify_cover_order(ExchOrderID="1100000017861430",LimitPrice=330)

#Note : For cover order just pass LimitPriceProfitOrder equal to Zero.
```

For Modifying LimitPriceProfitOrder 
```py
client.modify_bo_order(ExchOrderID="1100000017861430",TargetPrice=330)
client.modify_cover_order(ExchOrderID="1100000017861430",TargetPrice=330)
```
For Modifying TriggerPriceForSL
```py

client.modify_bo_order(ExchOrderID="1100000017861430",LimitPriceForSL=330)
client.modify_bo_order(ExchOrderID="1100000017861430",LimitPriceForSL=330)

#Note : You have pass atmarket=true while modifying stoploss price, Pass ExchorderId for the particular leg to modify.
```
#### Basket Orders

```py
# Create a new Basket
client.create_basket("<New Basket Name>")

# Rename existing basket
client.rename_basket("<Modified Basket Name>",<Exisiting Basket ID>)

# Clone existing basket
client.clone_basket(<Exisiting Basket ID>)

# Delete bulk baskets
delete_basket_list=[{"BasketID":"<Exisiting Basket ID>"},{"BasketID":"<Exisiting Basket ID>"}]
client.delete_basket(delete_basket_list)


# Get list of all baskets (Open/Closed)
client.get_basket()

basket_list= [
            {
                "BasketID": "<Exisiting Basket ID>"
            },
            {
                "BasketID": "<Exisiting Basket ID>"
            }
        ]
order_to_basket=Basket_order("N","C",23000,"BUY",1,"1660","I")
client.add_basket_order(order_to_basket,basket_list)

# Get orders in basket
client.get_order_in_basket(<Exisiting Basket ID>)

```

#### Fetching Order Status and Trade Information

```py
from py5paisa.order import  Exchange

req_list= [
        {
            "Exch": "N",
            "ExchType": "C",
            "ScripCode": 20374,
            "ExchOrderID": "1000000015310807"
        }]

# Fetches the trade details
client.fetch_trade_info(req_list)

req_list_= [

        {
            "Exch": "N",
            "RemoteOrderID": "90980441"
        }]
# Fetches the order status
client.fetch_order_status(req_list_)

# Fetch Trade History

print(client.get_trade_history("PASS EXCHANGE ORDER ID"))

```
#### Live Market Feed Streaming - Websocket
#NOTE : Webscoket only works with ScripCode
```py
req_list=[
            { "Exch":"N","ExchType":"C","ScripCode":1660},
            ]

req_data=client.Request_Feed('mf','s',req_list)
def on_message(ws, message):
    print(message)


client.connect(req_data)

client.receive_data(on_message)
```
Note: Use the following abbreviations :

Market Feed=mf

Market Depth (upto 5)=md

Indices (Spot Feed) =i

Open Interest=oi

Subscribe= s

Unsubscribe=u

#### Live Market Depth Streaming (Depth 20)

```py
a={
                "method":"subscribe",
                "operation":"20depth",
                "instruments":["NC2885"]
            }
print(client.socket_20_depth(a))
def on_message(ws, message):
    print(message)
client.receive_data(on_message)

Note:- Instruments in payload above is a list(array) in format as <exchange><exchange type><scrip code>
```

#### Level 5 Market Depth 
```py
print(client.fetch_market_depth_by_scrip(Exchange="N",ExchangeType="C",ScripCode="1660"))
print(client.fetch_market_depth_by_scrip(Exchange="N",ExchangeType="C",ScripData="RELIANCE_EQ"))
```

#### Full Market Snapshot 
```py
a=[{"Exchange":"N","ExchangeType":"C","ScripCode":"2885"},
   {"Exchange":"N","ExchangeType":"C","ScripData":"ITC_EQ"},
   ]
print(client.fetch_market_snapshot(a))
```


#### Option Chain
```py
client.get_expiry("N","NIFTY")
# Returns list of all active expiries

# client.get_option_chain("N","NIFTY",<Pass expiry timestamp from get_expiry response>)
client.get_option_chain("N","NIFTY",1647507600000)
```

#### Historical Data
```py
#historical_data(<Exchange>,<Exchange Type>,<Scrip Code>,<Time Frame>,<From Data>,<To Date>)

df=client.historical_data('N','C',1660,'15m','2021-05-25','2021-06-16')
print(df)

# Note : TimeFrame Should be from this list ['1m','5m','10m','15m','30m','60m','1d']
```


#### Bulk Order Placement

```py

bulk_order=[{
        "Exchange":"N", "ExchangeType":"C", "ScripCode":0, "ScripData":"ITC_EQ", "Price": "440", "OrderType": "Buy", "Qty": 1, "DisQty": "0", "StopLossPrice": "0", "IsIntraday": True, "iOrderValidity": "0", "RemoteOrderID":"50000091_220620"
    },{
        "Exchange":"N", "ExchangeType":"C", "ScripCode":0, "ScripData":"IDEA_EQ", "Price": "15", "OrderType": "Buy", "Qty": 1, "DisQty": "0", "StopLossPrice": "0", "IsIntraday": True, "iOrderValidity": "0", "RemoteOrderID":"50000091_220620"
    }
]
client.place_order_bulk(OrderList=bulk_order)
```

#### Strategy Execution
#### List Of Strategies Available
 - Short Straddle
 - Short Strangle
 - Long Straddle
 - Long Strangle
 - Iron Fly(Butterfly)
 - Iron Condor
 - Call Calendar Spread
 - Put Calendar Spread
 - Call Ladder
 - Put Ladder
 - Ladder
```py
#Import strategy package
from py5paisa.strategy import *
```
Note: These single-commands are capable of trading multiple legs of pre-defined strategies.
Like :- Short/Long Straddles and Strangles, Iron Fly and Iron Condor (many more to come)
Please use these at your own risk.
```py
#Create an Object:-
cred={
    "APP_NAME":"YOUR APP_NAME",
    "APP_SOURCE":YOUR APP_SOURCE,
    "USER_ID":"YOUR USER_ID",
    "PASSWORD":"YOUR PASSWORD",
    "USER_KEY":"YOUR USERKEY",
    "ENCRYPTION_KEY":"YOUR ENCRYPTION_KEY"
    }
--Old approach
strategy=strategies(user="random_email@xyz.com", passw="password", dob="YYYYMMDD",cred=cred)
--New Approach
strategy=strategies(cred=cred,request_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjUwMDUyNzcwIiwicm9sZSI6ImdpUUlvYXR5R2NYQUR3eFYwNXVXSGlPVzJRT1dOTGNzIiwibmJmIjoxNjY3ODMwODczLCJleHAiOjE2Njc4MzA5MDMsImlhdCI6MTY2NzgzMDg3M30.iP_FZtFy-nj6QeRd0sEhaKS-jr-wu-pCwtcdYCGPeO4")

```
Use the following to execute the strategy (note:- they are executed at market price only)
```py
#short_straddle(<symbol>,<strike price>,<qty>,<expiry>,<Order Type>)
strategy.short_straddle("banknifty",'37000','50','20210610','I',tag='<Your strategy Name>')

#Using tag is optional
```
```py
#short_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.short_strangle("banknifty",['35300','37000'],'50','20210610','D')
```
```py
#long_straddle(<symbol>,<strike price>,<qty>,<expiry>,<Order Type>)
strategy.long_straddle("banknifty",'37000','50','20210610','I',tag='<Your strategy Name>')

#Using tag is optional
```
```py
#long_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.long_strangle("banknifty",['35300','37000'],'50','20210610','D')
```

```py
#iron_condor(<symbol>,<List of buy strike prices>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.iron_condor("NIFTY",["15000","15200"],["15100","15150"],"75","20210603","I")
```

```py
#iron_fly(<symbol>,<List of buy strike prices>,<Sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.iron_fly("NIFTY",["15000","15200"],"15100","75","20210610","I",tag='<Your strategy Name>')

#Using tag is optional
```

```py
#call_calendar(<symbol>,<List of sell strike price>,<qty>,<list of expiry(first one will be bought and the second sold based on expiry)>,<Order Type>)
strategy.call_calendar("nifty",'15600','75',['20210603','20210610'],'I')
```

```py
#put_calendar(<symbol>,<List of sell strike price>,<qty>,<list of expiry(first one will be bought and the second sold based on expiry)>,<Order Type>)
strategy.put_calendar("nifty",'15600','75',['20210603','20210610'],'I')
```

```py
#call_ladder(<symbol>,<Buy strike prices>,<List of Sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.call_ladder("NIFTY","15100",["15300","15400"],"75","20210610","I")
```

```py
#put_ladder(<symbol>,<Buy strike prices>,<List of Sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.put_ladder("NIFTY","15000",["14800","14500"],"75","20210610","I",tag='<Your strategy Name>')

#Using tag is optional
```

```py
#ladder(<symbol>,<List of Buy strike prices>,<List of Sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.ladder("sbin",["400","420"],["350","370","450","500"],"1500","20210729","D")
```

```py
Squareoff a strategy Using tags
strategy.squareoff('tag')

# Use the same tag as used while executing the strategies
```



#### REPORTS

```py
TAX Report
a=client.tax_report("2024-01-01",'2024-06-26')
print(a)

# to fetch Tax report
```
```py
Ledger Report
a=client.fetch_ledger("2024-01-01",'2024-06-26')
print(a)

# to fetch Ledger report
```

#### TODO
 - Write tests.


#### Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template. -->
