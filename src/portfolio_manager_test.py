from unittest import TestCase
from src.portfolio_manager import PortfolioManager
from src.test_utils.fake_coinbase_pro_api import FakeCoinbaseProApi


class PortfolioManagerTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.__fake_coinbase_pro_api = FakeCoinbaseProApi()
        cls.__fake_coinbase_pro_api.set_fiat_balance(100)

        cls.__fake_coinbase_pro_api.set_quantity_held('BTC', 0)
        cls.__fake_coinbase_pro_api.set_quantity_held('ETH', 0)
        cls.__fake_coinbase_pro_api.set_quantity_held('LTC', 9)
        cls.__fake_coinbase_pro_api.set_quantity_held('DASH', 0)

        cls.__fake_coinbase_pro_api.set_symbol_quote('BTC', 500)
        cls.__fake_coinbase_pro_api.set_symbol_quote('ETH', 250)
        cls.__fake_coinbase_pro_api.set_symbol_quote('LTC', 100)
        cls.__fake_coinbase_pro_api.set_symbol_quote('DASH', 50)

        PortfolioManager(coinbase_pro_api=cls.__fake_coinbase_pro_api).set_portfolio_holdings([
            'BTC',
            'ETH'
        ])

    def test_holdings(self):
        self.assertEqual(1, self.__fake_coinbase_pro_api.get_quantity_held('BTC'))
        self.assertEqual(2, self.__fake_coinbase_pro_api.get_quantity_held('ETH'))
        self.assertEqual(0, self.__fake_coinbase_pro_api.get_quantity_held('LTC'))
        self.assertEqual(0, self.__fake_coinbase_pro_api.get_quantity_held('DASH'))

    def test_fiat_balance(self):
        self.assertEqual(0, self.__fake_coinbase_pro_api.get_fiat_balance())


