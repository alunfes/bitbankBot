from re import M
from ccxt.therock import therock
import socketio
import json
import logging
import time
import asyncio
import threading



class BitbankWSData:
    @classmethod
    def initialize(cls):
        cls.last_price = 0
        cls.lock_last_price = threading.Lock()
        cls.current_order_price = 999999999
        cls.lock_current_order_price = threading.Lock()
        cls.bidask = {}
        cls.lock_bidask = threading.Lock()
        cls.market_order_total_size = 0
        cls.locl_market_order_total_size = threading.Lock()

    @classmethod
    def set_last_price(cls, last_price):
        with cls.lock_last_price:
            cls.last_price = last_price
    
    @classmethod
    def get_last_price(cls):
        with cls.lock_last_price:
            return cls.last_price
    
    @classmethod
    def set_bidask(cls, bidask):
        with cls.lock_bidask:
            cls.bidask = bidask
    
    @classmethod
    def get_bidask(cls):
        with cls.lock_bidask:
            return cls.bidask
    
    @classmethod
    def set_current_order_price(cls, current_order_price):
        with cls.lock_current_order_price:
            cls.current_order_price = current_order_price
    
    @classmethod
    def get_current_order_price(cls):
        with cls.lock_current_order_price:
            return cls.current_order_price

    @classmethod
    def set_market_order_total_size(cls, market_order_total_size):
        with cls.locl_market_order_total_size:
            cls.market_order_total_size = market_order_total_size
    
    @classmethod
    def get_market_order_total_size(cls):
        with cls.market_order_total_size:
            return cls.market_order_total_size

class BitbankWS:
    def on_connect(self):
        print('bitbank socket connected')
        self.sio.on('message',self.on_data)
        self.sio.emit('join-room','ticker_btc_jpy')
        self.sio.emit('join-room','transactions_btc_jpy')
        self.sio.emit('join-room','depth_diff__btc_jpy')
        self.sio.emit('join-room','depth_whole_btc_jpy')
        
    def on_disconnect(self):
        print('bitbank socket disconnected')

    def on_data(self,data):
        if data['room_name'] == 'ticker_btc_jpy':
            BitbankWSData.set_last_price(int(data['message']['data']['last']))
        elif data['room_name'] == 'depth_whole_btc_jpy':
            print('ask:', data['message']['data']['asks'][0])
            print('bid:', data['message']['data']['bids'][0])
            BitbankWSData.set_bidask({'bid':int(data['message']['data']['bids'][0][0]), 'ask':int(data['message']['data']['asks'][0][0])})
            self.check_lastprice(int(data['message']['data']['asks'][0][0]), int(data['message']['data']['bids'][0][0]))
            self.check_largeorder(data['message']['data']['bids'])

    def check_lastprice(self, ask, bid):
        if BitbankWSData.get_current_order_price() > ask:
            if (ask - bid) > 1:
                BitbankWSData.set_current_order_price(ask-1)
            else:
                BitbankWSData.set_current_order_price(ask)
            print('update order price to ', BitbankWSData.get_current_order_price())
    
    def check_largeorder(self, bids):
        total_order_size = 0
        for i, bid in enumerate(bids):
            total_order_size += float(bid[1])
            if float(bid[1]) >= self.large_size_kijun and BitbankWSData.get_current_order_price() - int(bid[0]) <= self.large_size_pricediff_kijun:
                print('market sell to a large buy order.', bid, 'total order size=', total_order_size)
        BitbankWSData.set_market_order_total_size(total_order_size)
                
    def start(self):
        BitbankWSData.initialize()
        self.large_size_kijun = 5.0 #成り売りをぶつける大きな板のsize基準
        self.large_size_pricediff_kijun = 100 #成り売りをぶつける大きな板のcurrent order priceからの乖離幅の基準
        self.sio = socketio.Client(reconnection=True, reconnection_attempts=0, reconnection_delay=1, reconnection_delay_max=30)
        self.sio.on('connect', self.on_connect)
        self.sio.connect('wss://stream.bitbank.cc', transports = ['websocket'])
        #self.sio.wait()
    
    def stop(self):
        self.sio.reconnection = False
        self.sio.disconnect()


if __name__ == '__main__':
    bws = BitbankWS()
    bws.start()
    time.sleep(3)
    bws.sio.reconnection = False
    bws.sio.disconnect()
    #exit()