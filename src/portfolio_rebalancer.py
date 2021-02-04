from typing import Dict

from src.repositories.coinbase_pro_api import AbstractCoinbaseProApi
from src.repositories.nomics_api import AbstractNomicsApi


class PortfolioRebalancer:
    def __init__(self, coinbase_pro_api: AbstractCoinbaseProApi, nomics_api: AbstractNomicsApi):
        self.__coinbase_pro_api = coinbase_pro_api
        self.__nomics_api = nomics_api

    def rebalance(self) -> None:
        crypto_products: Dict[str, dict] = {
            product['base_currency']: product
            for product in self.__coinbase_pro_api.get_crypto_products()
        }
        symbols_to_hold = [
            x['symbol'] for x in
            sorted(
                self.__nomics_api.get_metrics(list(crypto_products.keys())),
                key=lambda x: float(x.get('market_cap', 0)),
                reverse=True
            )[:5]
        ]
        wallets: Dict[str, dict] = {w['currency']: w for w in self.__coinbase_pro_api.get_non_empty_crypto_wallets()}
        for symbol, wallet in wallets.items():
            self.__coinbase_pro_api.sell(
                crypto_products[symbol],
                float(wallet['available'])
            )
        liquidity = self.__coinbase_pro_api.get_cash_balance()
        target_balance: float = (liquidity / len(symbols_to_hold)) if symbols_to_hold else 0
        for symbol in symbols_to_hold:
            product = crypto_products[symbol]
            self.__coinbase_pro_api.buy(product, target_balance)
