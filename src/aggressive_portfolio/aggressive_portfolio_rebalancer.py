from src.environment import AbstractEnvironment
from src.portfolio_manager import AbstractPortfolioManager
from src.repositories.coinbase_pro_api import AbstractCoinbaseProApi
from src.repositories.nomics_api import AbstractNomicsApi


class AggressivePortfolioRebalancer:
    def __init__(
            self,
            coinbase_pro_api: AbstractCoinbaseProApi,
            nomics_api: AbstractNomicsApi,
            portfolio_manager: AbstractPortfolioManager,
            environment: AbstractEnvironment
    ):
        self.__coinbase_pro_api = coinbase_pro_api
        self.__nomics_api = nomics_api
        self.__portfolio_manager = portfolio_manager
        self.__environment = environment

    def rebalance(self):
        symbols = self.__coinbase_pro_api.get_tradeable_symbols()
        predictions = [
            {
                'symbol': x['id'],
                'prediction': float(x['predictions'][0]['price_change_pct'])
            }
            for x in self.__nomics_api.get_predictions(symbols)
        ]
        predictions = [x for x in predictions if x['prediction'] > 0]
        self.__portfolio_manager.set_portfolio_holdings([
            x['symbol'] for x in
            sorted(
                predictions,
                key=lambda p: p['prediction'],
                reverse=True
            )[:self.__environment.get_n_portfolio_holdings()]
        ])
