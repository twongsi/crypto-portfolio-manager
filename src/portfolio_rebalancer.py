from math import floor
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
        liquidity = self.__coinbase_pro_api.get_cash_balance() + sum([float(x['balance']) for x in wallets.values()])
        target_balance: float = (floor((liquidity / len(symbols_to_hold)) * 100) / 100) if symbols_to_hold else 0

        liquidate_symbols = [x for x in wallets.keys() if x not in symbols_to_hold]
        for liquidate_symbol in liquidate_symbols:
            self.__coinbase_pro_api.sell(
                crypto_products[liquidate_symbol],
                wallets[liquidate_symbol]['available']
            )

        sell_symbols = [x for x in wallets.keys() if x not in (liquidate_symbols + symbols_to_hold)]
        for sell_symbol in sell_symbols:
            wallet = wallets[sell_symbol]
            product = crypto_products[sell_symbol]
            existing_quantity = float(wallet['available'])
            if existing_quantity > 0:
                self.__coinbase_pro_api.sell(product, existing_quantity)
            self.__coinbase_pro_api.buy(product, target_balance)

        for buy_symbol in symbols_to_hold:
            wallet = wallets.get(buy_symbol, {})
            product = crypto_products[buy_symbol]
            exiting_quantity = float(wallet.get('available', 0))
            if exiting_quantity > 0:
                self.__coinbase_pro_api.sell(product, exiting_quantity)
            self.__coinbase_pro_api.buy(product, target_balance)
