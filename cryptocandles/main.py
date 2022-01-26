from typing import List

import pydantic_argparse
import requests

from cryptocandles.candlestick import Candlestick
from cryptocandles.settings import settings
from cryptocandles.utils import Arguments


def start():
    """Função responsável pela execução do programa"""
    s = requests.Session()
    parser = pydantic_argparse.ArgumentParser(
        model=Arguments,
        prog="CryptoCandle",
        description="Data aggregation in Candlesticks through the Poloniex API for sending to the Database",
        version="0.0.1",
    )
    args = parser.parse_typed_args()

    candle_list: List[Candlestick] = []

    for ticker in args.tickers:
        candle_list.extend([Candlestick(ticker, frequency=i) for i in (1, 5, 10)])

    while True:
        api_return_payload = s.get(settings.url_api_poloniex).json()  # Chamadas á API Poloniex

        for candle in candle_list:
            candle.set_attributes(float(api_return_payload[candle.crypto]['last']))  # Definindo dados dos Candles
            candle.save_candle_if_complete(
                float(api_return_payload[candle.crypto]['last']))  # Finalizando Candle e registrando


if __name__ == "__main__":
    start()
