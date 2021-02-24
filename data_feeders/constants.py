
# Mongodb Specifications
HOST = "localhost"
CONNECT_HOST = "127.0.0.1"
PORT = 27017
DB_NAME = "admin"
USERNAME = "User1"
PASSWORD = "user1"

# MongoDB Collection Name
COLLECTION_NAME = "BinanceTradingData"

# Input Data
# Add the symbol name in the list for which trade data needs 
# to be saved in the database
SYMBOL_LIST = ['bnbbtc', 'bnbusdt']

# Add the value of the price for which we need to check 
# the increase in price for a symbol
PRICE_INPUT = 267.22650000

# Binance Web-socket Stream URL and Keywords
MULTIPLE_STREAMS_URL = "wss://stream.binance.com:9443/stream?streams="
SINGLE_STREAM_URL = "wss://stream.binance.com:9443/ws/"
TRADE_KEY = "@trade/"