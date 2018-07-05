import asyncio
import websockets
import json
import sys
import requests, hashlib,time, urllib, hmac,datetime
import pandas as pd

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
        saveOrder(payload, msg, startprice)
        
        
def saveOrder(data, msg, startprice):
    data.update({'error':msg, 'exchange':'binance', 'startPrice':startprice})
    print(data)
    df = pd.DataFrame.from_records([data])
    appendDFToCSV_void(df, 'binanceOrders.csv', ',')
    
def appendDFToCSV_void(df, csvFilePath, sep=","):
    import os
    if not os.path.isfile(csvFilePath):
        df.to_csv(csvFilePath, mode='a', index=False, sep=sep)
    elif len(df.columns) != len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns):
        raise Exception("Columns do not match!! Dataframe has " + str(len(df.columns)) + " columns. CSV file has " + str(len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns)) + " columns.")
    elif not (df.columns == pd.read_csv(csvFilePath, nrows=1, sep=sep).columns).all():
        raise Exception("Columns and column order of dataframe and csv file do not match!!")
    else:
        df.to_csv(csvFilePath, mode='a', index=False, sep=sep, header=False)
        
#apikey = input("Enter API Key: ")
#secret = input("Enter Secret:")        
#asyncio.get_event_loop().run_until_complete(order(symbol = "BTCUSDT", quantity=1, price=7000, side='SELL', key=apikey, secret=secret)) 