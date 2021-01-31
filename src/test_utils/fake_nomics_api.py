from typing import List, Dict

from src.repositories.nomics_api import AbstractNomicsApi


class FakeNomicsApi(AbstractNomicsApi):
    def __init__(self):
        self.__predictions: Dict[str, float] = {}

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
