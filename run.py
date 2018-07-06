import binance
import trailers

#Start execution      
ordertype = input("Please select s for sell or b for buy: ")
assert (ordertype == 's' or ordertype == 'b'), "Wrong value"
trailerstop = float(input("Enter trailer stop value: "))
stoploss = float(input("Enter stop loss value: "))
orderdelta = float(input("Enter margin price for placing orders, ie. the delat from the last price: "))
quantity = float(input("Enter Quantity: "))
key = input("Enter API Key: ")
secret = input("Enter Secret:")
    
asyncio.get_event_loop().run_until_complete(tickerclient('BTCUSDT')) 