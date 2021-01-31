from abc import ABC, abstractmethod
from typing import List

import requests


class AbstractNomicsApi(ABC):
    @abstractmethod
    def get_predictions(self, symbols: List[str]) -> List[dict]:
        pass


class NomicsApi(AbstractNomicsApi):
    def get_predictions(self, symbols: List[str]) -> List[dict]:
        return requests.get(
            'https://nomics.com/data/currencies-predictions-ticker',
            params={'ids': ','.join(symbols)}
        ).json()
