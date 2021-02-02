from unittest import TestCase

from src.market_cap_portfolio.market_cap_portfolio_rebalancer import MarketCapPortfolioRebalancer
from src.repositories.nomics_api import AbstractNomicsApi
from src.test_utils.fake_coinbase_pro_api import FakeCoinbaseProApi
from src.test_utils.fake_environment import FakeEnvironment
from src.test_utils.fake_nomics_api import FakeNomicsApi
from src.test_utils.fake_portfolio_manager import FakePortfolioManager


class MarketCapPortfolioRebalancerTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.__fake_coinbase_pro_api = FakeCoinbaseProApi()
        cls.__fake_coinbase_pro_api.set_symbol_quote('FOO1', 100)
        cls.__fake_coinbase_pro_api.set_symbol_quote('FOO2', 101)
        cls.__fake_coinbase_pro_api.set_symbol_quote('FOO3', 102)
        cls.__fake_coinbase_pro_api.set_symbol_quote('FOO4', 103)
        cls.__fake_coinbase_pro_api.set_symbol_quote('FOO5', 104)
        cls.__fake_coinbase_pro_api.set_symbol_quote('FOO6', 105)
        cls.__fake_coinbase_pro_api.set_symbol_quote('FOO7', 106)
        cls.__fake_coinbase_pro_api.set_symbol_quote('FOO8', 107)
        cls.__fake_coinbase_pro_api.set_symbol_quote('FOO9', 108)
        cls.__fake_coinbase_pro_api.set_symbol_quote('FOO10', 109)
        cls.__fake_coinbase_pro_api.set_symbol_quote('BTC', 1000)
        cls.__fake_coinbase_pro_api.set_symbol_quote('ETH', 1001)
        cls.__fake_coinbase_pro_api.set_symbol_quote('LTC', 1002)

    def test_basic_case(self):
        fake_nomics_api = FakeNomicsApi()
        fake_nomics_api.set_market_cap('FOO1', 100)
        fake_nomics_api.set_market_cap('FOO2', 101)
        fake_nomics_api.set_market_cap('FOO3', 102)
        fake_nomics_api.set_market_cap('FOO4', 103)
        fake_nomics_api.set_market_cap('FOO5', 104)
        fake_nomics_api.set_market_cap('FOO6', 105)
        fake_nomics_api.set_market_cap('FOO7', 106)
        fake_nomics_api.set_market_cap('FOO8', 107)
        fake_nomics_api.set_market_cap('FOO9', 108)
        fake_nomics_api.set_market_cap('FOO10', 109)
        fake_nomics_api.set_market_cap('BTC', 1000)
        fake_nomics_api.set_market_cap('ETH', 1001)
        fake_nomics_api.set_market_cap('LTC', 1002)
        fake_portfolio_manager = self.__rebalance(fake_nomics_api)
        self.assertSetEqual({'LTC', 'ETH', 'BTC'}, set(fake_portfolio_manager.get_portfolio_holdings()))

    def test_just_hold_btc_if_no_outliers(self):
        fake_nomics_api = FakeNomicsApi()
        fake_nomics_api.set_market_cap('FOO1', 100)
        fake_nomics_api.set_market_cap('FOO2', 100)
        fake_nomics_api.set_market_cap('FOO3', 100)
        fake_nomics_api.set_market_cap('FOO4', 100)
        fake_nomics_api.set_market_cap('FOO5', 100)
        fake_nomics_api.set_market_cap('FOO6', 100)
        fake_nomics_api.set_market_cap('FOO7', 100)
        fake_nomics_api.set_market_cap('FOO8', 100)
        fake_nomics_api.set_market_cap('FOO9', 100)
        fake_nomics_api.set_market_cap('FOO10', 100)
        fake_nomics_api.set_market_cap('BTC', 100)
        fake_nomics_api.set_market_cap('ETH', 100)
        fake_nomics_api.set_market_cap('LTC', 100)
        fake_portfolio_manager = self.__rebalance(fake_nomics_api)
        self.assertSetEqual({'BTC'}, set(fake_portfolio_manager.get_portfolio_holdings()))

    def __rebalance(self, fake_nomics_api: AbstractNomicsApi) -> FakePortfolioManager:
        fake_portfolio_manager = FakePortfolioManager()
        MarketCapPortfolioRebalancer(
            coinbase_pro_api=self.__fake_coinbase_pro_api,
            nomics_api=fake_nomics_api,
            portfolio_manager=fake_portfolio_manager,
            environment=FakeEnvironment()
        ).rebalance()
        return fake_portfolio_manager
