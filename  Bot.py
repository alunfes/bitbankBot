import asyncio
from logging import log
import time
import datetime
import random

from BitbankWS import BitbankWS, BitbankWSData
from Trade import Trade
from TradeLog import TradeLog

class Bot:
    def initialize_order_var(self):
        self.order_price = 99999999
        self.order_size = 0
        self.order_id = ''
        self.exec_price = 0
        self.exec_size = 0
        self.exec_fee = 0
        self.exec_id_checked = []

    async def start(self):
        print('Started bot')
        self.initialize_order_var()
        TradeLog.initialize()
        self.last_market_order_timestamp = datetime.datetime.now().timestamp()
        self.suspend_after_market_order = 300 #sec
        self.trade = Trade()
        asyncio.run(self.trade.initialize())
        self.remaining_btc = float(asyncio.run(self.trade.get_total_assets())['BTC'])
        self.bws = BitbankWS()
        self.bws.start()
        self.bot_run_flg = True
        while self.bot_run_flg:
            #指値の変更が必要かを確認して指値を入れる
            if self.order_price > BitbankWSData.get_current_order_price():
                if self.order_id == '':
                    self.initialize_order_var()
                    self.order_id = self.trade.place_order('sell', 0.05, BitbankWSData.get_current_order_price(), 'limit')['order_id']
            #成り売りをぶつける板があるか確認して成り売りする
            if BitbankWSData.get_market_order_total_size() > 0:
                if self.order_id != '':#既存の指値があればそれをキャンセルする
                    self.trade.cancel_order(self.order_id)
                    await asyncio.sleep(1)
                    if self.trade.get_order_status(self.order_id) == 'canceled':
                        self.initialize_order_var()
                self.order_id = self.trade.place_order('sell', BitbankWSData.get_market_order_total_size(), 0, 'market')['order_id']
                self.last_market_order_timestamp = datetime.datetime.now().timestamp()
            #orderの約定確認
            if self.order_id != '':
                trades = self.trade.get_my_trades()
                for trade in trades:
                    if trade['info']['order_id'] == self.order_id and trade['info']['trade_id'] not in self.exec_id_checked:#約定処理
                        self.exec_id_checked.append(trade['info']['trade_id'])
                        self.exec_price = (self.exec_price * self.exec_size + float(trade['amount']) * float(trade['price'])) / (self.exec_size + float(trade['amount']))
                        self.order_size -= float(trade['amount'])
                        self.exec_size += float(trade['amount'])
                        self.exec_fee += float(trade['fee']['cost'])
                        self.remaining_btc -= float(trade['amount'])
                status = self.trade.get_order_status(self.order_id)
                if status == 'closed' or status == 'canceled':#取引の記録
                    TradeLog.log_trade(self.exec_price, self.exec_size, self.exec_fee)
                    self.initialize_order_var()
            #成り売り後は一定時間停止
            if self.last_market_order_timestamp > 0:
                self.last_market_order_timestamp = 0
                await asyncio.sleep(self.suspend_after_market_order) 
            await asyncio.sleep(1)
            #全ての売却が完了したら終了する
            if self.remaining_btc < 0.01:
                if self.order_id != '':
                    self.trade.cancel_order(self.order_id)
                self.trade.place_order('sell', float(self.trade.get_total_assets()['BTC']), 0, 'market')
                self.bws.stop()
                self.bot_run_flg = False
        #bot loop終了後に結果を表示する。
        print('completed!')
        print('Results')
        TradeLog.calc_ave()
        print('num trade=', TradeLog.num_trade)
        print('ave_price=', TradeLog.ave_price)
        print('cum_size=', TradeLog.total_size)
        print('cum_fee=', TradeLog.exec_cum_fee)

    async def get_limit_order_size(self):
        size = self.trade.get_total_assets()['BTC']
        



if __name__ == '__main__':
    try:
        asyncio.run(m.bitbank_websocket())
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass