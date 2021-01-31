from statistics import stdev, mean
from typing import List

from src.environment import AbstractEnvironment
from src.portfolio_manager import AbstractPortfolioManager
from src.repositories.coinbase_pro_api import AbstractCoinbaseProApi
from src.repositories.nomics_api import AbstractNomicsApi


class MarketCapPortfolioRebalancer:
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

    def rebalance(self) -> None:
        symbols = self.__coinbase_pro_api.get_tradeable_symbols()
        metrics = [x for x in self.__nomics_api.get_metrics(symbols) if 'market_cap' in x]
        market_caps: List[float] = [float(x['market_cap']) for x in metrics]
        market_cap_cutoff: float = mean(market_caps) + stdev(market_caps)
        self.__portfolio_manager.set_portfolio_holdings([
            x['symbol'] for x in metrics
            if float(x['market_cap']) > market_cap_cutoff
        ])
