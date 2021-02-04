from math import floor
from typing import Dict, List, Union

from src.repositories.coinbase_pro_api import AbstractCoinbaseProApi


class FakeCoinbaseProApi(AbstractCoinbaseProApi):
    def __init__(self, cash_balance: float, symbol_quotes: Dict[str, float]):
        self.__cash_balance: float = cash_balance
        self.__symbol_quantities_held: Dict[str, float] = {}
        self.__symbol_quotes = symbol_quotes

    def get_tradeable_crypto_simbles(self) -> List[str]:
        return list(set(list(self.__symbol_quotes.keys()) + list(self.__symbol_quantities_held.keys())))

    def get_cash_balance(self) -> float:
        return self.__cash_balance

    def get_non_empty_crypto_wallets(self) -> List[dict]:
        return [
            {
                'currency': k,
                'available': str(v),
            } for k, v in self.__symbol_quantities_held.items() if v > 0
        ]

    def buy(self, symbol: str, fiat_amount: Union[float, str]) -> None:
        fiat_amount = floor(float(fiat_amount) * 100) / 100
        assert fiat_amount <= self.__cash_balance
        quantity_bought = fiat_amount / self.__symbol_quotes[symbol]
        self.__symbol_quantities_held[symbol] = self.__symbol_quantities_held.get(symbol, 0) + quantity_bought
        self.__cash_balance -= fiat_amount

    def sell(self, symbol: str, quantity: Union[float, str]) -> None:
        quantity = float(quantity)
        assert quantity <= self.__symbol_quantities_held.get(symbol, 0)
        self.__symbol_quantities_held[symbol] -= quantity
        self.__cash_balance -= self.__symbol_quotes[symbol] * quantity

    def get_balance_held(self, symbol: str) -> float:
        return self.__symbol_quantities_held.get(symbol, 0) * self.__symbol_quotes.get(symbol, 0)

    def set_quantity_held(self, symbol: str, quantity: float) -> None:
        self.__symbol_quantities_held[symbol] = quantity
