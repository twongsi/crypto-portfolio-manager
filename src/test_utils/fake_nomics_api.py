from typing import List, Dict

from src.repositories.nomics_api import AbstractNomicsApi


class FakeNomicsApi(AbstractNomicsApi):

    def __init__(self, market_caps: Dict[str, float], prices: Dict[str, List[float]]):
        self.__market_caps = market_caps
        self.__prices = prices

    def get_metrics(self, symbols: List[str]) -> List[dict]:
        return [
            {
                'symbol': k,
                'market_cap': str(v)
            } for k, v in self.__market_caps.items()
        ]

    def get_recent_candles(self, symbol: str) -> List[dict]:
        return [
            {
                'close': str(price)
            } for price in self.__prices.get(symbol, [])
        ]
