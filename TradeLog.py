import datetime
import threading

class TradeLog:    
    @classmethod
    def initialize(cls):
        cls.num_trade = 0
        cls.exec_dt = []
        cls.lock_exec_dt = threading.Lock()
        cls.exec_price = []
        cls.lock_exec_price = threading.Lock()
        cls.exec_size = []
        cls.lock_exec_size = threading.Lock()
        cls.exec_fee = []
        cls.lock_exec_fee = threading.Lock()
        cls.exec_cum_fee = 0
        cls.ave_price = 0
        cls.total_size = 0

    @classmethod
    def __add_exec_dt(cls, dt):
        with cls.lock_exec_dt:
            cls.exec_dt.append(dt)
    @classmethod
    def get_exec_dt(cls):
        with cls.lock_exec_dt:
            return cls.exec_dt
    @classmethod
    def __add_exec_price(cls, price):
        with cls.lock_exec_price:
            cls.exec_price.append(price)
    @classmethod
    def get_exec_price(cls):
        with cls.lock_exec_price:
            return cls.exec_price
    @classmethod
    def __add_exec_size(cls, size):
        with cls.lock_exec_size:
            cls.exec_size.append(size)
    @classmethod
    def get_exec_size(cls):
        with cls.lock_exec_size:
            return cls.exec_size
    @classmethod
    def __add_exec_fee(cls, fee):
        with cls.lock_exec_fee:
            cls.exec_fee.append(fee)
    @classmethod
    def get_exec_fee(cls):
        with cls.lock_exec_fee:
            return cls.exec_fee

    @classmethod
    def log_trade(cls, exec_price, exec_size, exec_fee):
        cls.__add_exec_price(exec_price)
        cls.__add_exec_size(exec_size)
        cls.__add_exec_fee(exec_fee)
        cls.__add_exec_dt(datetime.datetime.now())
        cls.total_size += exec_size
        cls.exec_cum_fee += exec_fee
        cls.num_trade += 1

    @classmethod
    def calc_ave(cls):
        sum_v = 0
        for i,d in enumerate(cls.ave_price):
            sum_v += cls.exec_price[i] * cls.exec_size[i]
        cls.ave_price = sum_v / cls.total_size
