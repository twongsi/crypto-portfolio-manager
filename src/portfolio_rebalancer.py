from math import floor
from statistics import stdev
from typing import Dict, List, Optional

from src.emailer import AbstractEmailer
from src.environment import AbstractEnvironment
from src.repositories.coinbase_pro_api import AbstractCoinbaseProApi
from src.repositories.nomics_api import AbstractNomicsApi


class PortfolioRebalancer:
    def __init__(
            self,
            environment: AbstractEnvironment,
            coinbase_pro_api: AbstractCoinbaseProApi,
            nomics_api: AbstractNomicsApi,
            emailer: AbstractEmailer
    ):
        self.__environment = environment
        self.__coinbase_pro_api = coinbase_pro_api
        self.__nomics_api = nomics_api
        self.__emailer = emailer

    def rebalance(self) -> None:
        symbol_weights = self.__get_symbol_weights()
        self.__liquidate_all_positions()
        self.__set_holdings(symbol_weights)
        self.__send_email(symbol_weights)

    def __liquidate_all_positions(self) -> None:
        for wallet in self.__coinbase_pro_api.get_non_empty_crypto_wallets():
            self.__coinbase_pro_api.sell(wallet['currency'], float(wallet['available']))

    def __get_symbol_weights(self) -> Dict[str, float]:
        symbols = self.__coinbase_pro_api.get_crypto_symbols()
        symbols_to_hold = [
            x['symbol'] for x in
            sorted(
                self.__nomics_api.get_metrics(symbols),
                key=lambda x: float(x.get('market_cap', 0)),
                reverse=True
            )[:self.__environment.get_n_to_hold()]
        ]
        candles: Dict[str, List[dict]] = {
            symbol: self.__nomics_api.get_past_year_candles(symbol)
            for symbol in symbols_to_hold
        }
        inverse_volatilities: Dict[str, float] = {
            symbol: self.__calculate_inverse_volatility([float(x['close']) for x in candles[symbol]])
            for symbol in symbols_to_hold
        }
        total_inverse_volatility = sum(inverse_volatilities.values())
        return {
            symbol: inverse_volatility / total_inverse_volatility
            for symbol, inverse_volatility in inverse_volatilities.items()
        }

    def __set_holdings(self, symbol_weights: Dict[str, float]) -> None:
        total_liquidity = self.__coinbase_pro_api.get_cash_balance()
        for symbol, weight in symbol_weights.items():
            self.__coinbase_pro_api.buy(symbol, total_liquidity * weight)

    def __send_email(self, symbol_weights: Dict[str, float]) -> None:
        self.__emailer.send(
            self.__environment.get_email(),
            'Crypto portfolio has been rebalanced',
            '\n'.join([
                '%s (%s%%)' % (symbol, floor(weight * 1000) / 10)
                for symbol, weight in
                sorted(symbol_weights.items(), key=lambda x: x[1], reverse=True)
            ])
        )

    @staticmethod
    def __calculate_inverse_volatility(prices: List[float]) -> float:
        daily_returns: List[float] = []
        last_price: Optional[float] = None
        for price in prices:
            if last_price is not None:
                daily_returns.append((price / last_price) - 1)
            last_price = price
        return 1 / stdev(daily_returns)
