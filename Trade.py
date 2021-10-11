import asyncio
from hashlib import new
import ccxt
import time

class Trade:
    async def initialize(self):
        apis = await self.__read_api_key()
        self.bb = ccxt.bitbank({
            'apiKey': apis[0],
            'secret': apis[1],
        })

    async def __read_api_key(self):
        with open('./ignore/api.txt', 'r') as file:
            pub_key = file.readline().split(':')[1]
            pub_key = pub_key[:len(pub_key) - 1]
            secret_key = file.readline().split(':')[1]
            print('pub_key=', pub_key)
            print('secret_key=', secret_key)
            file.close()
            apis = [pub_key, secret_key]
            return apis

    '''
    {'id': '17468415197', 'clientOrderId': None, 'datetime': '2021-09-19T03:54:13.813Z', 'timestamp': 1632023653813, 'lastTradeTimestamp': None, 'status': 'open', 'symbol': 'BTC/JPY', 'type': 'limit', 'timeInForce': None, 'postOnly': None, 'side': 'sell', 'price': 5500000.0, 'stopPrice': None, 'cost': 0.0, 'average': 0.0, 'amount': 0.01, 'filled': 0.0, 'remaining': 0.01, 'trades': None, 'fee': None, 'info': {'order_id': '17468415197', 'pair': 'btc_jpy', 'side': 'sell', 'type': 'limit', 'start_amount': '0.0100', 'remaining_amount': '0.0100', 'executed_amount': '0.0000', 'price': '5500000', 'average_price': '0', 'ordered_at': '1632023653813', 'status': 'UNFILLED', 'expire_at': '1647575653813', 'post_only': False}, 'fees': []}
    '''
    async def place_order(self, order_side, order_size, order_price, order_type):
        order_id = ''
        if order_size >= 0.0001:
            try:
                if order_type == 'limit' or order_type == 'market':
                    order_id = self.bb.create_order(
                            symbol = 'btc_jpy',
                            #params={'pair': 'btc_jpy'},
                            type=order_type,
                            side=order_side,
                            price=order_price,
                            amount=order_size,
                        )
                else:
                    print('Invalid order type !')
            except Exception as e:
                print(e)
        else:
            print('Order size should be larger than 0.0001 !')
        print(order_id)
        return order_id

    '''
    {'order_id': '17468627405', 'pair': 'btc_jpy', 'side': 'sell', 'type': 'limit', 'start_amount': '0.0100', 'remaining_amount': '0.0100', 'executed_amount': '0.0000', 'price': '5500000', 'average_price': '0', 'ordered_at': '1632024652835', 'canceled_at': '1632024654821', 'status': 'CANCELED_UNFILLED', 'expire_at': '1647576652835', 'post_only': False}
    '''
    async def cancel_order(self, order_id):
        cancel = ''
        try:
            cancel = self.bb.cancel_order(id=order_id, symbol='btc_jpy', params={"pair": "btc_jpy"})
        except Exception as e:
                print(e)
        print(cancel)
        return cancel

    '''
    open
    '''
    async def get_order_status(self, order_id):
        order_status = ''
        try:
            order_status = self.bb.fetch_order_status(order_id, symbol='btc_jpy', params={})
        except Exception as e:
            print(e)
        return order_status


    '''
    [{'timestamp': 1632202101255, 'datetime': '2021-09-21T05:28:21.255Z', 'symbol': 'BTC/JPY', 'id': '1174043328', 'order': '17522353588', 'type': 'limit', 'side': 'sell', 'takerOrMaker': 'maker', 'price': 4637060.0, 'amount': 0.0059, 'cost': 27358.654, 'fee': {'currency': 'JPY', 'cost': -5.4717}, 'info': {'trade_id': '1174043328', 'order_id': '17522353588', 'pair': 'btc_jpy', 'side': 'sell', 'type': 'limit', 'amount': '0.0059', 'price': '4637060', 'maker_taker': 'maker', 'fee_amount_base': '0.00000000', 'fee_amount_quote': '-5.4717', 'executed_at': '1632202101255'}}, {'timestamp': 1632202103768, 'datetime': '2021-09-21T05:28:23.768Z', 'symbol': 'BTC/JPY', 'id': '1174043338', 'order': '17522353588', 'type': 'limit', 'side': 'sell', 'takerOrMaker': 'maker', 'price': 4637060.0, 'amount': 0.0041, 'cost': 19011.946, 'fee': {'currency': 'JPY', 'cost': -3.8024}, 'info': {'trade_id': '1174043338', 'order_id': '17522353588', 'pair': 'btc_jpy', 'side': 'sell', 'type': 'limit', 'amount': '0.0041', 'price': '4637060', 'maker_taker': 'maker', 'fee_amount_base': '0.00000000', 'fee_amount_quote': '-3.8024', 'executed_at': '1632202103768'}}]
    '''
    async def get_my_trades(self):
        trades = ''
        try:
            trades = self.bb.fetch_my_trades('btc_jpy')
        except Exception as e:
            print(e)
        return trades


    '''
    [{'id': '17521404717', 'clientOrderId': None, 'datetime': '2021-09-21T04:39:25.388Z', 'timestamp': 1632199165388, 'lastTradeTimestamp': None, 'status': 'open', 'symbol': 'BTC/JPY', 'type': 'limit', 'timeInForce': None, 'postOnly': None, 'side': 'sell', 'price': 5500000.0, 'stopPrice': None, 'cost': 0.0, 'average': 0.0, 'amount': 0.01, 'filled': 0.0, 'remaining': 0.01, 'trades': None, 'fee': None, 'info': {'order_id': '17521404717', 'pair': 'btc_jpy', 'side': 'sell', 'type': 'limit', 'start_amount': '0.0100', 'remaining_amount': '0.0100', 'executed_amount': '0.0000', 'price': '5500000', 'average_price': '0', 'ordered_at': '1632199165388', 'status': 'UNFILLED', 'expire_at': '1647751165388', 'post_only': False}, 'fees': []}, {'id': '17521405299', 'clientOrderId': None, 'datetime': '2021-09-21T04:39:27.398Z', 'timestamp': 1632199167398, 'lastTradeTimestamp': None, 'status': 'open', 'symbol': 'BTC/JPY', 'type': 'limit', 'timeInForce': None, 'postOnly': None, 'side': 'sell', 'price': 5510000.0, 'stopPrice': None, 'cost': 0.0, 'average': 0.0, 'amount': 0.01, 'filled': 0.0, 'remaining': 0.01, 'trades': None, 'fee': None, 'info': {'order_id': '17521405299', 'pair': 'btc_jpy', 'side': 'sell', 'type': 'limit', 'start_amount': '0.0100', 'remaining_amount': '0.0100', 'executed_amount': '0.0000', 'price': '5510000', 'average_price': '0', 'ordered_at': '1632199167398', 'status': 'UNFILLED', 'expire_at': '1647751167398', 'post_only': False}, 'fees': []}]
    '''
    async def get_open_orders(self):
        orders = []
        try:
            orders = self.bb.fetch_open_orders('btc_jpy')
        except Exception as e:
            print(e)
        return orders

    '''
    {'JPY': 3885.0096, 'BTC': 0.1, 'LTC': 0.0, 'XRP': 0.0, 'ETH': 0.0, 'MONA': 5.913e-05, 'BCH': 0.0, 'XLM': 0.0, 'QTUM': 0.0, 'BAT': 0.0, 'OMG': 0.0}
    '''
    async def get_total_assets(self):
        assets= {}
        try:
            assets = trade.bb.fetch_total_balance()
        except Exception as e:
            print(e)
        return assets


    



if __name__ == '__main__':
    trade = Trade()
    try:
        asyncio.run(trade.initialize())
        oid = asyncio.run(trade.place_order('sell', 0.01, 5500000, 'limit'))
        asyncio.run(trade.cancel_order(oid['id']))
        #print(asyncio.run(trade.get_total_assets()))
        #print(asyncio.run(trade.get_trade_history()))
        print(asyncio.run(trade.get_order_status(oid['id'])))
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass