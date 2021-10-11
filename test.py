import socketio
from Trade import Trade

class Test:
    '''
    現物のBTCやETHなどをできる限り高値で短期間に売り切るためのbot。
    小さめの指値を板の一番前に入れつつ、大きめの買い板が出現したら成行をぶつける。
    指値の大きさは0.01BTCを中心に毎回微妙に変える。
    価格が大きく下落した場合は売却を中断する。

    ・成り売りしたけど板が無くなったということが2回連続で続いたら成り売りを一定時間やめる。
    ・成り売りしたら一定時間指値も入れない状態を作るようにする。（5分くらい）
    '''
    def dotest(self):
        t = Trade()
        print(t.get_trade_history())

if __name__ == '__main__':
    t = Test()
    t.dotest()