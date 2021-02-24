import sys
import ast
import time
import json
import logging
import websocket

import constants
import mongo_client as db_client

logging.getLogger().setLevel(logging.INFO)


def main():
    """
        Get the inputs from constants file, connect to the Binance Web-Socket and handle web-socket connection
    """

    symbols = constants.SYMBOL_LIST
    if not symbols:
        logging.info("No symbol entered to continue.")
        sys.exit()

    try:
        input_price = float(constants.PRICE_INPUT)
    except ValueError:
        logging.error("That wasn't a number!")

    data_feeder = DataFeeder(symbols, input_price)

    def on_message(ws, message, data_feeder):
        """
            This function is called when a message is received by the web-socket.
        """
        data_feeder.store_trading_data_into_db(data=data_feeder.process_received_message(message))

    def on_error(ws, error):
        """
            This function is called when there is an error in the web-socket connection.
        """
        logging.error("Error:-", error)

    def on_close(ws):
        """
            This function is called when the web-socket connection is closed.
        """
        logging.info("### Web-socket Connection Closed ###")

    try:
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(data_feeder.url,
                                on_message = lambda ws, message: on_message(ws, message, data_feeder),
                                on_error = on_error,
                                on_close = on_close)
        ws.run_forever()
    except Exception as e:
        logging.error('Could not connect to web-socket',str(e))


class InputFormatError(Exception):
    """Custom exception class for our error"""
    pass


class DataFeeder(object):
    """
        This class process the stream data and later stores it in the mongo DB.

    """
    def __init__(self, symbols, input_price):
        """
            Initializing data and creating mongo class object
            Args:
                symbols(sting) - The symbols taken as an input from user
                input_price(float) - The input price taken as an input from user

            Return:
                None
        """
        self.mongo_db = db_client.initilize_database(
            db_user=constants.USERNAME, db_password=constants.PASSWORD
        )
        self.url = self.get_stream_url(symbols)
        self.input_price = input_price


    def store_trading_data_into_db(self, data=None, collection_name="BinanceTradingData"):
        """
            This functions creates a dictionary with the stream data and saved in the Monogo database
            Args:
                data(dict) = Formatted data from fetched from the web-socket
                collection_name(string) = The name of collection in which the data needs to be stored

            Return:
                None
        """

        if data:
            trading_data = {
                "event type": data.get("e"),
                "event time": data.get("E"),
                "symbol": data.get("s"),
                "timestamp": data.get("t"),
                "price": data.get("p"),
                "quantity": data.get("q"),
                "buyer order ID": data.get("b"),
                "seller order ID": data.get("a"),
                "trade time": data.get("T")
            }
            self.check_symbol_price(trading_data)
            logging.info(trading_data)
            logging.info("-------------------")
            self.mongo_db.insert_in_background(trading_data, collection_name)

    def process_received_message(self, message):
        """
            This function formats the data received from web-socket to python native.
            Args:
                message(string) - This is the data received from web-socket

            Return:
                It returns a data dictionary after processing the web-socket message
        """
        try:
            trade_data = json.loads(message)
            trade_data[u'data'].pop(u'm')
            trade_data[u'data'].pop(u'M')
            trade_data = ast.literal_eval(json.dumps(trade_data))
            return trade_data.get('data')
        except:
            logging.error('Error while processing received websocket message.')
            raise InputFormatError('Could not process the websocket input')

    def check_symbol_price(self, data):
        """
            This function checks the input price and price fetched from trade stream for the
            given symbol

            Args:
                data(dict) - This is the formated data parameter fetched from Binance trade stream

            Return:
                None
        """
        if self.input_price < float(data.get("price")):
            logging.info("Symbol price is higher than the input provided by the user.")
            logging.info("Input Price :- ")
            logging.info(str(self.input_price))
            logging.info("Symbol Price :- ")
            logging.info(str(data.get("price")))
            logging.info("+++++++++++++++++++++++++++++")

    def get_stream_url(self, symbols):
        """
            Generate stream URL according to the input

            Args:
                symbols (String)- It is input taken from them user

            Return:
                It return the stream URL to connect to Binance web-socket
        """

        if len(symbols) > 0:
            streams = ""
            for symbol in symbols:
                streams += symbol.lower() + constants.TRADE_KEY
            streams = streams[:-1]
            url = constants.MULTIPLE_STREAMS_URL + streams
        else:
            stream = symbols[0] + constants.TRADE_KEY
            url = constants.SINGLE_STREAM_URL + stream
        return url



if __name__ == "__main__":
    main()