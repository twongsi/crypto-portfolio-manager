from typing import Dict
from unittest import TestCase

from src.portfolio_rebalancer import PortfolioRebalancer
from src.test_utils.fake_coinbase_pro_api import FakeCoinbaseProApi
from src.test_utils.fake_nomics_api import FakeNomicsApi


def __cryptocurrency(quote: float, market_cap: float, min_sell_quantity: float, min_buy_funds: float) -> dict:
    return {
        'quote': quote,
        'market_cap': market_cap,
        'min_sell_quantity': min_sell_quantity,
        'min_buy_funds': min_buy_funds
    }


cryptocurrencies: Dict[str, dict] = {
    'BTC': __cryptocurrency(quote=36571.03, market_cap=999, min_sell_quantity=0.001, min_buy_funds=5),
    'ETH': __cryptocurrency(quote=1543.34, market_cap=998, min_sell_quantity=0.001, min_buy_funds=5),
    'LTC': __cryptocurrency(quote=0.999319, market_cap=997, min_sell_quantity=0.1, min_buy_funds=10),
    'LINK': __cryptocurrency(quote=0.379226, market_cap=996, min_sell_quantity=1, min_buy_funds=10),
    'BCH': __cryptocurrency(quote=17.29, market_cap=995, min_sell_quantity=0.01, min_buy_funds=10),
    'XLM': __cryptocurrency(quote=0.430767, market_cap=994, min_sell_quantity=1, min_buy_funds=0.1)
}

liquidity: float = 2000.99


class PortfolioRebalancerTest(TestCase):
    def test_from_no_holdings(self):
        fake_coinbase_pro_api = self.__get_fake_coinbase_pro_api(liquidity)
        self.__rebalance(fake_coinbase_pro_api)
        self.__assert(fake_coinbase_pro_api)

    def test_removal_of_currency(self):
        existing_holding_balance = 10
        fake_coinbase_pro_api = self.__get_fake_coinbase_pro_api(liquidity - existing_holding_balance)
        fake_coinbase_pro_api.set_quantity_held('XLM', existing_holding_balance / cryptocurrencies['XLM']['quote'])
        self.__rebalance(fake_coinbase_pro_api)
        self.__assert(fake_coinbase_pro_api)

    def test_buy(self):
        existing_holding_balance = 394.19
        fake_coinbase_pro_api = self.__get_fake_coinbase_pro_api(liquidity - existing_holding_balance)
        fake_coinbase_pro_api.set_quantity_held('BTC', existing_holding_balance / cryptocurrencies['BTC']['quote'])
        self.__rebalance(fake_coinbase_pro_api)
        self.__assert(fake_coinbase_pro_api)

    def test_minimum_buy(self):
        existing_holding_balance = 395.3
        fake_coinbase_pro_api = self.__get_fake_coinbase_pro_api(liquidity - existing_holding_balance)
        fake_coinbase_pro_api.set_quantity_held('BTC', existing_holding_balance / cryptocurrencies['BTC']['quote'])
        self.__rebalance(fake_coinbase_pro_api)
        self.__assert(fake_coinbase_pro_api)

    def test_sell(self):
        existing_holding_balance = 500
        fake_coinbase_pro_api = self.__get_fake_coinbase_pro_api(liquidity - existing_holding_balance)
        fake_coinbase_pro_api.set_quantity_held('BTC', existing_holding_balance / cryptocurrencies['BTC']['quote'])
        self.__rebalance(fake_coinbase_pro_api)
        self.__assert(fake_coinbase_pro_api)

    def test_minimum_sell(self):
        existing_holding_balance = 436.7
        fake_coinbase_pro_api = self.__get_fake_coinbase_pro_api(liquidity - existing_holding_balance)
        fake_coinbase_pro_api.set_quantity_held('BTC', existing_holding_balance / cryptocurrencies['BTC']['quote'])
        self.__rebalance(fake_coinbase_pro_api)
        self.__assert(fake_coinbase_pro_api)

    def __assert(self, fake_coinbase_pro_api: FakeCoinbaseProApi):
        for symbol in ['BTC', 'ETH', 'LTC', 'LINK', 'BCH']:
            with self.subTest('should hold', symbol=symbol):
                self.assertLess(
                    abs(400.19 - fake_coinbase_pro_api.get_quantity_held(symbol) * cryptocurrencies[symbol]['quote']),
                    1
                )

        with self.subTest('should sell all of XLM'):
            self.assertEqual(0, fake_coinbase_pro_api.get_quantity_held('XLM'))

        with self.subTest('should have minimal cash leftover'):
            self.assertLess(fake_coinbase_pro_api.get_cash_balance(), 1)

    @staticmethod
    def __rebalance(fake_coinbase_pro_api: FakeCoinbaseProApi) -> None:
        PortfolioRebalancer(
            coinbase_pro_api=fake_coinbase_pro_api,
            nomics_api=FakeNomicsApi(
                market_caps={k: v['market_cap'] for k, v in cryptocurrencies.items()}
            )
        ).rebalance()

    @staticmethod
    def __get_fake_coinbase_pro_api(cash_balance: float) -> FakeCoinbaseProApi:
        return FakeCoinbaseProApi(
            cash_balance=cash_balance,
            symbol_quotes={k: v['quote'] for k, v in cryptocurrencies.items()},
            crypto_products=[
                {
                    'base_currency': k,
                    'base_min_size': str(v['min_sell_quantity']),
                    'min_market_funds': str(v['min_buy_funds'])
                } for k, v in cryptocurrencies.items()
            ]
        )
