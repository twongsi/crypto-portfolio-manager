from typing import List

import requests
from cbpro import AuthenticatedClient

from src.env import get_env, Env


class PredictionService:
    def __init__(self, cbp: AuthenticatedClient):
        self.__cbp = cbp

    def get_top_currencies(self) -> List[dict]:
        products = self.__cbp.get_products()
        symbols = [x['base_currency'] for x in products if x['quote_currency'] == 'USD']
        predictions = self.__get_predictions(symbols)
        predictions = [p for p in predictions if p['prediction'] > 0]
        n_portfolio_holdings = int(get_env(Env.N_PORTFOLIO_HOLDINGS))
        return sorted(predictions, key=lambda p: p['prediction'], reverse=True)[:n_portfolio_holdings]

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
