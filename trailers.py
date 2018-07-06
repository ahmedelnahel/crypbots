import asyncio
import websockets
import json
import sys
from binance import order

lastprice=0.0
stop = 0.0
entryprice = 0.0

async def tickerclient(symbol):
    s = symbol.lower()
    async with websockets.connect(
            f"wss://stream.binance.com:9443/ws/{s}@ticker") as websocket:
        async for message in websocket:
            if(await trailer(message, symbol, websocket)):
                break
            
async def trailer(message, symbol,  websocket):
    global lastprice, stop, stoploss, quantity, orderdelta, key, secret,entryprice
    ticker = json.loads(message)
    #print last price
    tickerPrice = float(ticker['c'])
    if(lastprice == 0):
        entryprice = tickerPrice
        
    if (lastprice != tickerPrice):
        print(tickerPrice)
        if(tickerPrice > lastprice and ordertype =='s' ):
            stop = tickerPrice - trailerstop
        elif (ordertype =='b' and (tickerPrice < lastprice or lastprice == 0)):
            stop = tickerPrice + trailerstop
            
        if(ordertype =='s' and tickerPrice < lastprice and (tickerPrice < stop or tickerPrice < stoploss)):
            await order(symbol.upper(), quantity, tickerPrice-orderdelta, 'SELL', key, secret, entryprice)
            print("sell order")
            return True
        elif(ordertype =='b' and tickerPrice > lastprice and (tickerPrice > stop or tickerPrice > stoploss)):
            #buy
            await order(symbol.upper(), quantity, tickerPrice + orderdelta, 'BUY', key, secret, entryprice)
            print("buy order")
            return True
        
        lastprice = tickerPrice
    return False
        




