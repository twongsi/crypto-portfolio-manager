from src.environment import Environment
from src.portfolio_rebalancer import PortfolioRebalancer
from src.repositories.coinbase_pro_api import CoinbaseProApi
from src.repositories.nomics_api import NomicsApi


def main():
    environment = Environment()
    PortfolioRebalancer(
        coinbase_pro_api=CoinbaseProApi(
            key=environment.get_coinbase_api_key(),
            secret=environment.get_coinbase_api_secret(),
            passphrase=environment.get_coinbase_api_passphrase()
        ),
        nomics_api=NomicsApi()
    ).rebalance()


if __name__ == '__main__':
    main()
