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

        balance_adjustments_by_symbol: Dict[str, float] = {
            symbol: (target_balance if symbol in symbols_to_hold else 0) -
                    float(wallets.get(symbol, {}).get('balance', 0))
            for symbol in
            symbols_to_hold + list(wallets.keys())
        }

        liquidate_symbols = [x for x in balance_adjustments_by_symbol.keys() if x not in symbols_to_hold]
        for liquidate_symbol in liquidate_symbols:
            self.__coinbase_pro_api.sell(
                crypto_products[liquidate_symbol],
                wallets[liquidate_symbol]['available']
            )

        sell_symbols = [k for k, v in balance_adjustments_by_symbol.items() if v < 0 and k not in liquidate_symbols]
        for sell_symbol in sell_symbols:
            wallet = wallets[sell_symbol]
            product = crypto_products[sell_symbol]
            current_quantity = float(wallet['available'])
            implied_current_price = float(wallet['balance']) / current_quantity
            sell_quantity = -balance_adjustments_by_symbol[sell_symbol] / implied_current_price
            if sell_quantity >= float(product['base_min_size']):
                self.__coinbase_pro_api.sell(product, sell_quantity)
            else:
                self.__coinbase_pro_api.sell(crypto_products[sell_symbol], current_quantity)
                self.__coinbase_pro_api.buy(product, target_balance)

        buy_symbols = [k for k, v in balance_adjustments_by_symbol.items() if v > 0]
        for buy_symbol in buy_symbols:
            wallet = wallets.get(buy_symbol, {})
            product = crypto_products[buy_symbol]
            buy_funds = target_balance - float(wallet.get('balance', 0))
            if buy_funds >= float(product['min_market_funds']):
                self.__coinbase_pro_api.buy(product, buy_funds)
            else:
                self.__coinbase_pro_api.sell(crypto_products[buy_symbol], float(wallet['available']))
                self.__coinbase_pro_api.buy(product, target_balance)
