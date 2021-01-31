from abc import ABC, abstractmethod
from typing import List

from src.repositories.coinbase_pro_api import AbstractCoinbaseProApi


class AbstractPortfolioManager(ABC):
    @abstractmethod
    def set_portfolio_holdings(self, symbols: List[str]) -> None:
        pass


class PortfolioManager(AbstractPortfolioManager):
    def __init__(self, coinbase_pro_api: AbstractCoinbaseProApi):
        self.__coinbase_pro_api = coinbase_pro_api

    def set_portfolio_holdings(self, symbols: List[str]) -> None:
        self.__liquidate_all_holdings()
        self.__hold_equal_amounts(symbols)

    def __liquidate_all_holdings(self) -> None:
        for account in self.__coinbase_pro_api.get_active_crypto_wallets():
            self.__coinbase_pro_api.sell(account['currency'], account['available'])

    def __hold_equal_amounts(self, symbols: List[str]) -> None:
        if not symbols:
            return
        usd_account = self.__coinbase_pro_api.get_usd_wallet()
        liquidity: float = float(usd_account['balance'])
        liquidity_per_holding: float = liquidity / len(symbols)
        for symbol in symbols:
            print('Buying $%s of %s' % (liquidity_per_holding, symbol))
            self.__coinbase_pro_api.buy(symbol, liquidity_per_holding)
