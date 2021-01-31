from src.environment import Environment
from src.market_cap_portfolio.market_cap_portfolio_rebalancer import MarketCapPortfolioRebalancer
from src.repositories.coinbase_pro_api import CoinbaseProApi
from src.repositories.nomics_api import NomicsApi
from src.portfolio_manager import PortfolioManager


def main():
    environment = Environment()
    coinbase_pro_api = CoinbaseProApi(environment=environment)
    MarketCapPortfolioRebalancer(
        coinbase_pro_api=coinbase_pro_api,
        nomics_api=NomicsApi(),
        portfolio_manager=PortfolioManager(coinbase_pro_api=coinbase_pro_api),
        environment=environment
    ).rebalance()


if __name__ == '__main__':
    main()
