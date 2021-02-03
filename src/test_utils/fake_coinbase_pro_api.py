from typing import Dict, List, Union

from src.repositories.coinbase_pro_api import AbstractCoinbaseProApi


class FakeCoinbaseProApi(AbstractCoinbaseProApi):
    def __init__(self, cash_balance: float, symbol_quotes: Dict[str, float], crypto_products: List[dict]):
        self.__cash_balance: float = cash_balance
        self.__symbol_quantities_held: Dict[str, float] = {}
        self.__symbol_quotes = symbol_quotes
        self.__crypto_products = crypto_products

    def get_crypto_products(self) -> List[dict]:
        return self.__crypto_products

    def get_cash_balance(self) -> float:
        return self.__cash_balance

    def get_non_empty_crypto_wallets(self) -> List[dict]:
        return [
            {
                'currency': k,
                'available': str(v),
                'balance': str(v * self.__symbol_quotes[k])
            } for k, v in self.__symbol_quantities_held.items() if v > 0
        ]

    def buy(self, product: dict, fiat_amount: Union[float, str]) -> None:
        symbol = product['base_currency']
        fiat_amount = float(fiat_amount)
        assert fiat_amount <= self.__cash_balance
        assert fiat_amount >= float(product['min_market_funds'])
        quantity_bought = fiat_amount / self.__symbol_quotes[symbol]
        self.__symbol_quantities_held[symbol] = self.__symbol_quantities_held.get(symbol, 0) + quantity_bought
        self.__cash_balance -= fiat_amount

    def sell(self, product: dict, quantity: Union[float, str]) -> None:
        symbol = product['base_currency']
        quantity = float(quantity)
        assert quantity <= self.__symbol_quantities_held[symbol]
        assert quantity >= float(product['base_min_size'])
        self.__symbol_quantities_held[symbol] -= quantity
        self.__cash_balance += self.__symbol_quotes[symbol] * quantity

    def get_quantity_held(self, symbol: str) -> float:
        return self.__symbol_quantities_held.get(symbol, 0)

    def set_quantity_held(self, symbol: str, quantity: float) -> None:
        self.__symbol_quantities_held[symbol] = quantity
