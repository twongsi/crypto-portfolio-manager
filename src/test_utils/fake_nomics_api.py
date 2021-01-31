from typing import List, Dict

from src.repositories.nomics_api import AbstractNomicsApi


class FakeNomicsApi(AbstractNomicsApi):
    def __init__(self):
        self.__predictions: Dict[str, float] = {}
        self.__market_caps: Dict[str, float] = {}

    def get_predictions(self, symbols: List[str]) -> List[dict]:
        return [
            {
                'id': k,
                'predictions': [
                    {
                        'price_change_pct': str(v)
                    }
                ]
            }
            for k, v in self.__predictions.items()
            if k in symbols
        ]

    def set_prediction(self, symbol: str, prediction: float) -> None:
        self.__predictions[symbol] = prediction

    def get_metrics(self, symbols: List[str]) -> List[dict]:
        metrics: List[dict] = [
            {
                'symbol': k,
                'market_cap': str(v)
            } for k, v in self.__market_caps.items()
        ]
        metrics.append({
            'symbol': 'No Market Cap'
        })
        return metrics

    def set_market_cap(self, symbol: str, market_cap: float) -> None:
        self.__market_caps[symbol] = market_cap
