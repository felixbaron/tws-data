# https://tradersacademy.online/trading-topics/trader-workstation-tws/receiving-market-data-and-historical-candlesticks
import datetime
import os
import threading
from time import sleep

from ibapi.client import BarData, EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

from src.database.helper import update_schema, save_row
from src.tws.helper import convert_to_dict, save_dict_to_file

symbols = None


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, req_id, error_code, error_string: str):
        print("Log message: ", error_string)
        pass

    def tickString(self, req_id, tick_type, value: str):
        ratio_dict = convert_to_dict(value)
        filename = "./" + str(req_id) + ".kpis.dict"
        save_dict_to_file(filename, ratio_dict)
        update_schema(schema_file=filename)
        save_row(
            database="stock_data",
            symbol=symbols[req_id],
            market="NASDAQ",
            table="symbols",
            csv_file=filename,
        )
        os.remove(filename)

    def historicalData(self, req_id: int, bar: BarData):
        pricing = dict(date_time=bar.date, price=bar.close)
        filename = "./" + str(req_id) + ".prices.dict"
        save_dict_to_file(filename, pricing)

    def historicalDataEnd(self, req_id: int, start: str, end: str):
        filename = "./" + str(req_id) + ".prices.dict"
        save_row(
            database="stock_data",
            symbol=symbols[req_id],
            market="NASDAQ",
            table="prices",
            csv_file=filename,
        )
        os.remove(filename)


def get_contract(symbol, exchange):
    """Get fundamentals for stock"""
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = exchange
    return contract


def get_historical_performance(ticker_id, symbol, exchange, days: int):
    """Get historical data"""
    global app
    # queryTime = (datetime.datetime.today() - datetime.timedelta(days=days)).strftime(
    #     "%Y%m%d %H:%M:%S"
    # )
    contract = get_contract(symbol, exchange)
    app.reqHistoricalData(
        ticker_id,
        contract,
        "",
        "6 M",
        "1 day",
        "MIDPOINT",
        1,
        1,
        False,
        [],
    )


def fetch_ratios_and_save_to_disk(ticker_id, symbol, exchange):
    global app
    # Get contract
    contract = get_contract(symbol, exchange)
    # app.reqMktData(1, contract, 'mdoff,233,236,47,258,292', False, False, [])
    app.reqMktData(ticker_id, contract, "mdoff,258", False, False, [])


def run_loop():
    app.run()


def run_ibapi(symbols_param):
    global symbols
    symbols = symbols_param

    # Connect to TWS
    # app.connect("127.0.0.1", 7496, 1)

    # Connect to Gateway
    app.connect("127.0.0.1", 4001, 1)
    app.reqMarketDataType(4)

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()


def stop_ibapi():
    global app
    app.disconnect()


app = IBapi()
