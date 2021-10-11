import asyncio
import time
import BitbankWS
import Trade

class Master:
    async def main(self):
        pass
        
        

if __name__ == '__main__':
    m = Master()
    try:
        asyncio.run(m.bitbank_websocket())
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass