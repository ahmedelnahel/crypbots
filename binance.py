import asyncio
import websockets
import json
import sys
import requests, hashlib,time, urllib, hmac,datetime
import tradestore

#side accepts BUY or SELL
async def order(symbol, quantity, price, side, key, secret, startprice):
    msg =''
    ts =  int(round(time.time() * 1000))
    payload = {"symbol":symbol, "quantity":quantity,'price':price, 'side':side, 'type':'LIMIT','timeInForce':"GTC", "timestamp":ts}
    
    try:    
        params = f"symbol={symbol}&quantity={quantity}&price={price}&side={side}&type=LIMIT&timeInForce=GTC&timestamp={ts}"
        hashedsig = hmac.new(secret.encode('utf-8'), params.encode('utf-8'), hashlib.sha256).hexdigest()
        payload.update({'signature':hashedsig})
        print(payload)
        headers = {'X-MBX-APIKEY': key}
        resp = requests.post('https://api.binance.com/api/v3/order', data=payload, headers=headers)
        respjson = resp.json()
        print (resp.status_code)
        print (resp.json())
        if resp.status_code != 400:
            # This means something went wrong.
            msg = respjson['msg']
            raise Exception('POST /tasks/ {}'.format(resp.status_code))
        
        if(respjson['msg']):
            msg = respjson['msg']
            raise Exception('Order error: ', respjson['msg'])
        elif(respjson['orderId']):
            print(respjson['orderId'])
    finally:
        tradestore.saveOrder(payload, msg, startprice)
        
        

        
#apikey = input("Enter API Key: ")
#secret = input("Enter Secret:")        
#asyncio.get_event_loop().run_until_complete(order(symbol = "BTCUSDT", quantity=1, price=7000, side='SELL', key=apikey, secret=secret)) 