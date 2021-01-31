from math import floor
from typing import List

from cbpro import AuthenticatedClient


class PortfolioManager:
    def __init__(self, cbp: AuthenticatedClient):
        self.__cbp = cbp

    def set_portfolio_holdings(self, symbols: List[str]) -> None:
        # TODO: fees are killing me. make this more transaction-efficient than just liquidating and re-buying.
        self.__liquidate_all_holdings()
        self.__hold_equal_amounts(symbols)

    def __liquidate_all_holdings(self) -> None:
        accounts = [
            x for x in self.__cbp.get_accounts()
            if x['currency'] != 'USD' and float(x['available']) > 0
        ]
        for account in accounts:
            self.__cbp.place_market_order(
                product_id='%s-USD' % account['currency'],
                side='sell',
                size=account['available']
            )

    def __hold_equal_amounts(self, symbols: List[str]) -> None:
        if not symbols:
            return
        usd_account = next(
            x for x in self.__cbp.get_accounts()
            if x['currency'] == 'USD'
        )
        liquidity: float = float(usd_account['balance'])
        liquidity_per_holding: float = liquidity / len(symbols)
        liquidity_per_holding = floor(liquidity_per_holding * 100) / 100
        for symbol in symbols:
            print('Buying $%s of %s' % (liquidity_per_holding, symbol))
            self.__cbp.place_market_order(
                product_id='%s-USD' % symbol,
                side='buy',
                funds=str(liquidity_per_holding)
            )
