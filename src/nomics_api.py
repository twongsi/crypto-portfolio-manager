from abc import ABC, abstractmethod
from typing import List

import requests


class AbstractNomicsApi(ABC):
    @abstractmethod
    def get_metrics(self, symbols: List[str]) -> List[dict]:
        pass

    @abstractmethod
    def get_candles(self, symbol: str) -> List[dict]:
        pass


class NomicsApi(AbstractNomicsApi):

    def get_metrics(self, symbols: List[str]) -> List[dict]:
        return requests.get(
            'https://nomics.com/data/currencies-ticker',
            params={
                'quote-currency': 'USD',
                'symbols': ','.join(symbols)
            }
        ).json()['items']

    def get_candles(self, symbol: str) -> List[dict]:
        return requests.get(
            'https://nomics.com/data/candles',
            params={
                'currency': symbol,
                'interval': '365d'
            }
        ).json()
