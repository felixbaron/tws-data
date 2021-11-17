from database.helper import (
    connect_database,
    fixtures,
    enhance_schema,
    update_schema,
)
from tws.connection import (
    fetch_ratios_and_save_to_disk,
    run_ibapi,
    stop_ibapi,
    get_historical_performance,
)
from tws.helper import convert_to_dict, read_csv_to_dict, save_dict_to_file
from database.helper import save_row
from time import sleep
import os

ratio_file = "./ratios.csv"
is_create_fixtures = False
is_fetch_data = True
symbols = ["FB", "SNOW", "CRM", "AAPL", "ADBE", "EA", "GOOG", "NFLX", "NVDA"]
market = "NASDAQ"


if is_create_fixtures:
    fixtures(
        is_create_db=True,
        is_create_table=True,
    )
    file_name = "./prices.dict"
    save_dict_to_file(
        file_name, dict(symbol=symbols[0], price=7.7, date_time="21")
    )
    update_schema(schema_file="./prices.dict")
    os.remove(file_name)

if is_fetch_data:
    run_ibapi(symbols)
    for symbol in symbols:
        ticker_id = symbols.index(symbol)
        fetch_ratios_and_save_to_disk(ticker_id, symbol, market)
        get_historical_performance(ticker_id, symbol=symbol, exchange=market, days=180)
    sleep(30)
    stop_ibapi()
