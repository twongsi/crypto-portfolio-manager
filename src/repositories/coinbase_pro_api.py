from abc import ABC, abstractmethod
from math import floor
from typing import List, Union

from cbpro import AuthenticatedClient


class AbstractCoinbaseProApi(ABC):
    @abstractmethod
    def get_crypto_products(self) -> List[dict]:
        pass

    @abstractmethod
    def get_cash_balance(self) -> float:
        pass

    @abstractmethod
    def get_non_empty_crypto_wallets(self) -> List[dict]:
        pass

    @abstractmethod
    def buy(self, product: dict, fiat_amount: Union[float, str]) -> None:
        pass

    @abstractmethod
    def sell(self, product: dict, quantity: Union[float, str]) -> None:
        pass


class CoinbaseProApi(AbstractCoinbaseProApi):
    def __init__(self, key: str, secret: str, passphrase: str):
        self.__cbp_client = AuthenticatedClient(key, secret, passphrase)

    def get_crypto_products(self) -> List[dict]:
        products = self.__cbp_client.get_products()
        return [x for x in products if x['quote_currency'] == 'USD']

    def get_cash_balance(self) -> float:
        return float(next(x for x in self.__cbp_client.get_accounts() if x['currency'] == 'USD')['balance'])

    def get_non_empty_crypto_wallets(self) -> List[dict]:
        return [
            x for x in self.__cbp_client.get_accounts()
            if x['currency'] != 'USD' and float(x['available']) > 0
        ]

    def buy(self, product: dict, fiat_amount: Union[float, str]) -> None:
        fiat_amount = float(fiat_amount)
        fiat_amount = floor(fiat_amount * 100) / 100
        self.__cbp_client.place_market_order(
            product_id=product['id'],
            side='buy',
            funds=str(fiat_amount)
        )

    def sell(self, product: dict, quantity: Union[float, str]) -> None:
        self.__cbp_client.place_market_order(
            product_id=product['id'],
            side='sell',
            size=str(quantity)
        )
