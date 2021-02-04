from typing import Dict
from unittest import TestCase

from src.portfolio_rebalancer import PortfolioRebalancer
from src.test_utils.fake_coinbase_pro_api import FakeCoinbaseProApi
from src.test_utils.fake_environment import FakeEnvironment
from src.test_utils.fake_nomics_api import FakeNomicsApi


def __cryptocurrency(quote: float, market_cap: float, price_stdev: float) -> dict:
    return {
        'quote': quote,
        'market_cap': market_cap,
        'price_stdev': price_stdev
    }


BTC = 'BTC'
ETH = 'ETH'
LTC = 'LTC'
LINK = 'LINK'
BCH = 'BCH'
XLM = 'XLM'

cryptocurrencies: Dict[str, dict] = {
    BTC: __cryptocurrency(quote=36571.03, market_cap=999, price_stdev=7),
    ETH: __cryptocurrency(quote=1543.34, market_cap=998, price_stdev=6),
    LTC: __cryptocurrency(quote=0.999319, market_cap=997, price_stdev=5),
    LINK: __cryptocurrency(quote=0.379226, market_cap=996, price_stdev=4),
    BCH: __cryptocurrency(quote=17.29, market_cap=995, price_stdev=3),
    XLM: __cryptocurrency(quote=0.430767, market_cap=994, price_stdev=2)
}


class PortfolioRebalancerTest(TestCase):
    def test_from_empty_portfolio(self):
        fake_coinbase_pro_api = self.__get_fake_coinbase_pro_api()
        self.__rebalance(fake_coinbase_pro_api)
        self.__assert_common(fake_coinbase_pro_api)

    def test_liquidation_of_currency_not_in_top_n_by_market_cap(self):
        fake_coinbase_pro_api = self.__get_fake_coinbase_pro_api()
        fake_coinbase_pro_api.set_quantity_held(XLM, 1)
        self.__rebalance(fake_coinbase_pro_api)
        self.__assert_common(fake_coinbase_pro_api)

    def test_adjustment_of_existing_holding(self):
        fake_coinbase_pro_api = self.__get_fake_coinbase_pro_api()
        fake_coinbase_pro_api.set_quantity_held(BTC, 0.01)
        self.__rebalance(fake_coinbase_pro_api)
        self.__assert_common(fake_coinbase_pro_api)

    def test_n_to_hold_configurability_minus_1(self):
        fake_coinbase_pro_api = self.__get_fake_coinbase_pro_api()
        self.__rebalance(fake_coinbase_pro_api, 4)
        self.assertEqual(0, fake_coinbase_pro_api.get_balance_held(BCH))

    def test_n_to_hold_configurability_plus_1(self):
        fake_coinbase_pro_api = self.__get_fake_coinbase_pro_api()
        self.__rebalance(fake_coinbase_pro_api, 6)
        self.assertGreater(fake_coinbase_pro_api.get_balance_held(XLM), 0)

    def __assert_common(self, fake_coinbase_pro_api: FakeCoinbaseProApi):
        for symbol in [BTC, ETH, LTC, LINK, BCH]:
            with self.subTest('should hold', symbol=symbol):
                self.assertGreater(fake_coinbase_pro_api.get_balance_held(symbol), 0)

        with self.subTest('should hold balances proportional to volatility'):
            bch_balance = fake_coinbase_pro_api.get_balance_held(BCH)
            link_balance = fake_coinbase_pro_api.get_balance_held(LINK)
            ltc_balance = fake_coinbase_pro_api.get_balance_held(LTC)
            eth_balance = fake_coinbase_pro_api.get_balance_held(ETH)
            btc_balance = fake_coinbase_pro_api.get_balance_held(BTC)
            self.assertGreater(bch_balance, link_balance)
            self.assertGreater(link_balance, ltc_balance)
            self.assertGreater(ltc_balance, eth_balance)
            self.assertGreater(eth_balance, btc_balance)

        with self.subTest('should not hold XLM'):
            self.assertEqual(0, fake_coinbase_pro_api.get_balance_held(XLM))

        with self.subTest('should have minimal cash leftover'):
            self.assertLess(fake_coinbase_pro_api.get_cash_balance(), 1)

    @staticmethod
    def __rebalance(fake_coinbase_pro_api: FakeCoinbaseProApi, n_to_hold: int = 5) -> None:
        PortfolioRebalancer(
            environment=FakeEnvironment(n_to_hold=n_to_hold),
            coinbase_pro_api=fake_coinbase_pro_api,
            nomics_api=FakeNomicsApi(
                market_caps={k: v['market_cap'] for k, v in cryptocurrencies.items()},
                prices={
                    k: [1 for _ in range(v['price_stdev'])] + [1 + v['price_stdev'] for _ in range(v['price_stdev'])]
                    for k, v in cryptocurrencies.items()
                }
            )
        ).rebalance()

    @staticmethod
    def __get_fake_coinbase_pro_api() -> FakeCoinbaseProApi:
        return FakeCoinbaseProApi(
            cash_balance=1000,
            symbol_quotes={k: v['quote'] for k, v in cryptocurrencies.items()}
        )
