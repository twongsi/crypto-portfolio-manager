from typing import List

import requests
from cbpro import AuthenticatedClient


class PredictionService:
    def __init__(self, cbp: AuthenticatedClient):
        self.__cbp = cbp

    def get_top_currencies(self, top_n: int = 5) -> List[dict]:
        products = self.__cbp.get_products()
        symbols = [x['base_currency'] for x in products if x['quote_currency'] == 'USD']
        predictions = self.__get_predictions(symbols)
        predictions = [p for p in predictions if p['prediction'] > 0]
        return sorted(predictions, key=lambda p: p['prediction'], reverse=True)[:top_n]

    @staticmethod
    def __get_predictions(symbols: List[str]) -> List[dict]:
        raw: List[dict] = requests.get(
            'https://nomics.com/data/currencies-predictions-ticker',
            params={'ids': ','.join(symbols)}
        ).json()

        return [
            {
                'symbol': x['id'],
                'prediction': float(x['predictions'][0]['price_change_pct']),
                'prediction_start': x['predictions'][0]['timestamp_start'],
                'prediction_end': x['predictions'][0]['timestamp_end']
            } for x in raw
        ]
