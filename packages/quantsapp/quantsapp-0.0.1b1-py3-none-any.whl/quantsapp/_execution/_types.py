# Built-in Modules
import typing


# ----------------------------------------------------------------------------------------------------




# -- Broker Orders -----------------------------------------------------------------------------------



# class OrderListingApiResponseData(typing.TypedDict):
#     """sample
#     ```
#     {
#         'broker_client': 'mstock,MA6232931',
#         'b_orderid': '33422505073382',
#         'qty': 75,
#         'price': 1.2,
#         'buy_sell': 'b',
#         'instrument': 'NIFTY:15-May-25:c:25500',
#         'order_type': 'limit',
#         'product_type': 'nrml',
#         'q_usec': 1746596369775443,
#         'userid': 622594,
#         'order_status': 'pending',
#         'b_usec_update': 1746596370000000,
#         'e_orderid': 1600000075847609,
#         'o_ctr': 1,
#         'qty_filled': 0,
#         'stop_price': 0.0
#     }
#     """
#     broker_client: str
#     b_orderid: generic_types.NumericString  # BrokerID when placing order
#     qty: int
#     price: float
#     buy_sell: typing.Literal['b', 's']
#     instrument: str
#     order_type: OrderTypes
#     product_type: ProductTypes
#     q_usec: int  # Quantsapp Order Send Timestamp in ms
#     userid: int  # User ID of client who placed the order
#     order_status: OrderStatus
#     b_usec_update: int  # Broker Order Updation Timestamp in ms
#     e_orderid: int  # Another BrokerID when placing order
#     o_ctr: int  # Order Update counter
#     qty_filled: int
#     stop_price: float


# class GetOrdersAccountWiseApiResponse(typing.TypedDict):
#     """sample
#     ```
#     {
#         'status': '1',
#         'msg': 'success',
#         'gzip': True,
#         'orders': 'H4sIAOsVG2gC/02Qy27DIBBFfyVinUSYZ+xdN5WySFfdVFWFbEwrFPwIDAur6r+XsdsorGDunTPDff8mXZyuLhobvBuBNDsyJJjsdX95UoyzmldkvyOdmWLvou/RwLlgTFJJNecnhvINliJoWa5z9NaVR3Vk2JcXk1wI2Nah048JYh7+Rr2cn1/fmkoeLu1yYLKxDZOSUjSu8wwsM8JI8IMHsuKnPlu4C2McwrqByclZnKuFkrXiqtZaCsGLVpRtc1XWrsUdnqCFnJAyu7H349f2UwSZPPctuAeeptspFvcQRqW2spYnoRWtEW4sRJS2YMynD8GhF3tLtrP5z4ge6c/HL86ik8+DAQAA',
#         'pagination_key': typing.Any  # Optional, only available if more records are there (current limit is 100)
#     }
#     """
#     status: ApiResponseStatus
#     msg: str
#     gzip: bool
#     orders: str | list[OrderListingApiResponseData]
#     pagination_key: typing.Optional[typing.Any]








# class PositionsCombinedApiResponseData(typing.TypedDict):
#     """sample
#     ```
#     {
#         'instrument': 'NIFTY:15-May-25:c:25200',
#         'product_type': 'nrml',
#         'buy_qty': 75,
#         'buy_t_value': 581.25,
#         'sell_qty': 75,
#         'sell_t_value': 570
#     }
#     """
#     instrument: str
#     product_type: ProductTypes
#     buy_qty: int
#     buy_t_value: int | float
#     sell_qty: int
#     sell_t_value: int | float

# class PositionsAccountwiseApiResponseData(typing.TypedDict):
#     """sample
#     ```
#     {
#         'mstock,MA6232931': [
#             {
#                 'instrument': 'NIFTY:15-May-25:c:25900',
#                 'product_type': 'nrml',
#                 'buy_qty': 75,
#                 'buy_t_value': 93.75,
#                 'sell_qty': 75,
#                 'sell_t_value': 86.25
#                 'p_ctr': 3,
#             },
#         ]
#     }
#     """
#     instrument: str  # TODO change this to instrument type
#     product_type: ProductTypes
#     buy_qty: int
#     buy_t_value: int | float
#     sell_qty: int
#     sell_t_value: int | float
#     p_ctr: int


# class GetPositionsApiResponse(typing.TypedDict):
#     """sample
#     ```
#     {
#         "status": "1",
#         "msg": "success",
#         "gzip": true,
#         "positions": "H4sIABvKIWgC/4uuVsrMKy4pKs1NzStRslJQ8vN0C4m0MjTV9U2s1DUytUq2MjI1MjBQ0lFQKijKTylNLokvqSxIBSnNK8rNAYknlVbGF5ZUAoXMTaHckviyxJxSkCpTC0M9I5BwcWpODrIyMB9JnblBbSwAX3B17I4AAAA=",
#     }
#     """
#     status: ApiResponseStatus
#     msg: str
#     gzip: bool
#     positions: str | list[PositionsCombinedApiResponseData | PositionsAccountwiseApiResponseData]







# class UpdateOrderBookApiResponse(typing.TypedDict):
#     """sample
#     ```
#     {
#         "status": "1",
#         "msg": "Orderbook Updated !",
#         "orders_response": {
#             "status": "1",
#             "msg": "success",
#             "gzip": true,
#             "orders": "H4sIAJ4pI2gC/72Su07DMBSGX6Xy3Fa+5DhONhYkhjKxIISs1DGS1VxaxxkixLvj45YKEAMhEp7sc/5z+T/56ZXsde9r611NyhURAjgHCkxkheBkvSJ73x+s16ZxtgsoaYfQm8N6dyO54IVgSaTHwRo9Husq2ChieZYzLhUUNB2UjJMebNNgiz3W2E9zmUwyViiqsgJkTLtuCH5sL0Pv724fHksGm101bTiUpuQAlGKfXpvgo0bgHTvqIVRhHLDMVJ2JM21NrskwHXFD0rjWBQwfvTMYoVsK6dnXowlXXefbBmWnZPFnb6cwxUQO56t+cWlkbBkDsersUUawRfa2Xn1HzvkHcsXpUuSczkUuhMoY/RPybDHyfA7yz96WIWfygjxXdOEvZ7jaPOQUJCiVdv/3X8627NfEv1qbQ/z5HYpc1iFYBAAA"
#         },
#         "trade_status": "1",
#         "trade_msg": "Tradebook Updated !",
#         "positions_status": "1",
#         "positions_msg": "Positions Updated !",
#     }
#     {
#         "status": "1",
#         "msg": "Orderbook Updated !",
#         "positions_response": {
#             "status": "1",
#             "msg": "success",
#             "gzip": true,
#             "positions": "H4sIANUpI2gC/4uOBQApu0wNAgAAAA=="
#         },
#         "trade_status": "1",
#         "trade_msg": "Tradebook Updated !",
#         "positions_status": "1",
#         "positions_msg": "Positions Updated !",
#     }
#     """
#     status: ApiResponseStatus
#     msg: str
#     trade_status: str
#     trade_msg: str
#     positions_status: str
#     positions_msg: str

#     orders_response: typing.Optional[GetOrdersAccountWiseApiResponse]
#     positions_response: typing.Optional[GetPositionsApiResponse]


