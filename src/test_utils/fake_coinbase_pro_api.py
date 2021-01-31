from typing import Dict, List, Union

from src.repositories.coinbase_pro_api import AbstractCoinbaseProApi


class FakeCoinbaseProApi(AbstractCoinbaseProApi):
    def __init__(self):
        self.__fiat_balance: float = 0.0
        self.__symbol_quantities_held: Dict[str, float] = {}
        self.__symbol_quotes: Dict[str, float] = {}

    def get_tradeable_symbols(self) -> List[str]:
        return list(self.__symbol_quotes.keys())

    def get_usd_wallet(self) -> dict:
        return {
            'balance': str(self.__fiat_balance)
        }

    def get_active_crypto_wallets(self) -> List[dict]:
        return [
            {
                'currency': k,
                'available': str(v)
            } for k, v in self.__symbol_quantities_held.items()
        ]

    def buy(self, symbol: str, fiat_amount: Union[float, str]) -> None:
        fiat_amount = float(fiat_amount)
        assert fiat_amount <= self.__fiat_balance
        quantity_bought = fiat_amount / self.__symbol_quotes[symbol]
        self.__symbol_quantities_held[symbol] = self.__symbol_quantities_held.get(symbol, 0) + quantity_bought
        self.__fiat_balance -= fiat_amount

    def sell(self, symbol: str, quantity: Union[float, str]) -> None:
        quantity = float(quantity)
        assert quantity <= self.__symbol_quantities_held[symbol]
        self.__symbol_quantities_held[symbol] -= quantity
        self.__fiat_balance += self.__symbol_quotes[symbol] * quantity

    def set_symbol_quote(self, symbol: str, quote: float) -> None:
        self.__symbol_quotes[symbol] = quote

    def get_quantity_held(self, symbol: str) -> float:
        return self.__symbol_quantities_held[symbol]

    def set_quantity_held(self, symbol: str, quantity: float) -> None:
        self.__symbol_quantities_held[symbol] = quantity

    def get_fiat_balance(self) -> float:
        return self.__fiat_balance

    def set_fiat_balance(self, fiat_balance: float) -> None:
        self.__fiat_balance = fiat_balance