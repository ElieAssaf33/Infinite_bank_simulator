import requests

btc = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
data = requests.get(btc) 
data = data.json() 
btc = data['price']

eth = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
data = requests.get(eth) 
data = data.json() 
eth = data['price']

doge = "https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT"
data = requests.get(doge) 
data = data.json() 
doge = data['price']

sol = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
data = requests.get(sol) 
data = data.json() 
sol = data['price']

avax = "https://api.binance.com/api/v3/ticker/price?symbol=AVAXUSDT"
data = requests.get(avax) 
data = data.json() 
avax = data['price']

ada = "https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT"
data = requests.get(ada) 
data = data.json() 
ada = data['price']

xrp = "https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT"
data = requests.get(xrp) 
data = data.json() 
xrp = data['price']

lite = "https://api.binance.com/api/v3/ticker/price?symbol=LTCUSDT"
data = requests.get(lite) 
data = data.json() 
lite = data['price']

polygon = "https://api.binance.com/api/v3/ticker/price?symbol=MATICUSDT"
data = requests.get(polygon) 
data = data.json() 
polygon = data['price']


prices = {"Bitcoin":btc, "Ethereum": eth, 
"Dogecoin": doge, "Solana":sol, 
"Avalanche": avax, "Cardano": ada,
"XRP": xrp, "Litecoin": lite, "Polygon": polygon}

