from unittest import TestCase

from src.aggressive_portfolio.aggressive_portfolio_rebalancer import AggressivePortfolioRebalancer
from src.repositories.nomics_api import AbstractNomicsApi
from src.test_utils.fake_coinbase_pro_api import FakeCoinbaseProApi
from src.test_utils.fake_environment import FakeEnvironment
from src.test_utils.fake_nomics_api import FakeNomicsApi
from src.test_utils.fake_portfolio_manager import FakePortfolioManager


class AggressivePortfolioRebalancerTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.__fake_coinbase_pro_api = FakeCoinbaseProApi()
        cls.__fake_coinbase_pro_api.set_symbol_quote('BTC', 0)
        cls.__fake_coinbase_pro_api.set_symbol_quote('ETH', 0)
        cls.__fake_coinbase_pro_api.set_symbol_quote('LTC', 0)
        cls.__fake_coinbase_pro_api.set_symbol_quote('DASH', 0)
        cls.__fake_coinbase_pro_api.set_symbol_quote('WTF', 0)

    def test_basic_case(self):
        fake_nomics_api = FakeNomicsApi()
        fake_nomics_api.set_prediction('BTC', 1)
        fake_nomics_api.set_prediction('ETH', 2)
        fake_nomics_api.set_prediction('LTC', 3)
        fake_nomics_api.set_prediction('DASH', 4)
        fake_portfolio_manager = self.__rebalance(fake_nomics_api)
        self.assertEqual(['DASH', 'LTC'], fake_portfolio_manager.get_portfolio_holdings())

    def test_no_positive_predictions(self):
        fake_nomics_api = FakeNomicsApi()
        fake_nomics_api.set_prediction('BTC', 0)
        fake_nomics_api.set_prediction('ETH', -1)
        fake_nomics_api.set_prediction('LTC', -2)
        fake_nomics_api.set_prediction('DASH', -3)
        fake_portfolio_manager = self.__rebalance(fake_nomics_api)
        self.assertEqual([], fake_portfolio_manager.get_portfolio_holdings())

    def test_less_than_n_portfolio_holdings(self):
        fake_nomics_api = FakeNomicsApi()
        fake_nomics_api.set_prediction('BTC', 1)
        fake_nomics_api.set_prediction('ETH', -1)
        fake_nomics_api.set_prediction('LTC', -1)
        fake_nomics_api.set_prediction('DASH', -1)
        fake_portfolio_manager = self.__rebalance(fake_nomics_api)
        self.assertEqual(['BTC'], fake_portfolio_manager.get_portfolio_holdings())

    def __rebalance(self, fake_nomics_api: AbstractNomicsApi) -> FakePortfolioManager:
        fake_portfolio_manager = FakePortfolioManager()
        AggressivePortfolioRebalancer(
            coinbase_pro_api=self.__fake_coinbase_pro_api,
            nomics_api=fake_nomics_api,
            portfolio_manager=fake_portfolio_manager,
            environment=FakeEnvironment(n_portfolio_holdings=2)
        ).rebalance()
        return fake_portfolio_manager
