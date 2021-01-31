from typing import List

from src.portfolio_manager import AbstractPortfolioManager


class FakePortfolioManager(AbstractPortfolioManager):
    def __init__(self):
        self.__portfolio_holdings: List[str] = []

    def set_portfolio_holdings(self, symbols: List[str]) -> None:
        self.__portfolio_holdings = symbols

    def get_portfolio_holdings(self) -> List[str]:
        return self.__portfolio_holdings