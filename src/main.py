import src.env as env
from src.portfolio_rebalancer import PortfolioRebalancer
from src.coinbase_pro_api import CoinbaseProApi
from src.nomics_api import NomicsApi


def main():
    PortfolioRebalancer(
        coinbase_pro_api=CoinbaseProApi(
            key=env.get_coinbase_api_key(),
            secret=env.get_coinbase_api_secret(),
            passphrase=env.get_coinbase_api_passphrase()
        ),
        nomics_api=NomicsApi()
    ).rebalance()


if __name__ == '__main__':
    main()
