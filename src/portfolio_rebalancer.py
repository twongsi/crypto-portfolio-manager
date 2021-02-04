from statistics import stdev
from typing import Dict, List, Optional

from src.coinbase_pro_api import AbstractCoinbaseProApi
from src.nomics_api import AbstractNomicsApi


class PortfolioRebalancer:
    def __init__(self, coinbase_pro_api: AbstractCoinbaseProApi, nomics_api: AbstractNomicsApi):
        self.__coinbase_pro_api = coinbase_pro_api
        self.__nomics_api = nomics_api

    def rebalance(self) -> None:
        symbols = self.__coinbase_pro_api.get_crypto_symbols()
        symbols_to_hold = [
            x['symbol'] for x in
            sorted(
                self.__nomics_api.get_metrics(symbols),
                key=lambda x: float(x.get('market_cap', 0)),
                reverse=True
            )[:5]
        ]
        candles: Dict[str, List[dict]] = {
            symbol: self.__nomics_api.get_candles(symbol)
            for symbol in symbols_to_hold
        }

        for wallet in self.__coinbase_pro_api.get_non_empty_crypto_wallets():
            self.__coinbase_pro_api.sell(wallet['currency'], float(wallet['available']))

        inverse_volatilities: Dict[str, float] = {
            symbol: self.__calculate_inverse_volatility([float(x['close']) for x in candles[symbol]])
            for symbol in symbols_to_hold
        }
        total_inverse_volatility = sum(inverse_volatilities.values())
        total_liquidity = self.__coinbase_pro_api.get_cash_balance()
        for symbol, inverse_volatility in sorted(inverse_volatilities.items(), key=lambda x: x[1], reverse=True):
            weight = inverse_volatility / total_inverse_volatility
            buy_amount = total_liquidity * weight
            self.__coinbase_pro_api.buy(symbol, buy_amount)

    @staticmethod
    def __calculate_inverse_volatility(prices: List[float]) -> float:
        daily_returns: List[float] = []
        last_price: Optional[float] = None
        for price in prices:
            if last_price is not None:
                daily_returns.append((price / last_price) - 1)
            last_price = price
        return 1 / stdev(daily_returns)
