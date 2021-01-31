from abc import ABC, abstractmethod
from math import floor
from typing import List, Union

from cbpro import AuthenticatedClient

from src.environment import AbstractEnvironment


class AbstractCoinbaseProApi(ABC):
    @abstractmethod
    def get_tradeable_symbols(self) -> List[str]:
        pass

    @abstractmethod
    def get_usd_wallet(self) -> dict:
        pass

    @abstractmethod
    def get_active_crypto_wallets(self) -> List[dict]:
        pass

    @abstractmethod
    def buy(self, symbol: str, fiat_amount: Union[float, str]) -> None:
        pass

    @abstractmethod
    def sell(self, symbol: str, quantity: Union[float, str]) -> None:
        pass


class CoinbaseProApi(AbstractCoinbaseProApi):
    def __init__(self, environment: AbstractEnvironment):
        self.__cbp_client = AuthenticatedClient(
            environment.get_coinbase_api_key(),
            environment.get_coinbase_api_secret(),
            environment.get_coinbase_api_passphrase()
        )

    def get_tradeable_symbols(self) -> List[str]:
        products = self.__cbp_client.get_products()
        return [x['base_currency'] for x in products if x['quote_currency'] == 'USD']

    def get_usd_wallet(self) -> dict:
        return next(
            x for x in self.__cbp_client.get_accounts()
            if x['currency'] == 'USD'
        )

    def get_active_crypto_wallets(self) -> List[dict]:
        return [
            x for x in self.__cbp_client.get_accounts()
            if x['currency'] != 'USD' and float(x['available']) > 0
        ]

    def buy(self, symbol: str, fiat_amount: Union[float, str]) -> None:
        fiat_amount = float(fiat_amount)
        fiat_amount = floor(fiat_amount * 100) / 100
        self.__cbp_client.place_market_order(
            product_id='%s-USD' % symbol,
            side='buy',
            funds=str(fiat_amount)
        )

    def sell(self, symbol: str, quantity: Union[float, str]) -> None:
        self.__cbp_client.place_market_order(
            product_id='%s-USD' % symbol,
            side='sell',
            size=str(quantity)
        )


