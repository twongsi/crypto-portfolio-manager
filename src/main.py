from typing import List

from cbpro import AuthenticatedClient

from src.env import get_env, Env
from src.portfolio_manager import PortfolioManager
from src.prediction_service import PredictionService


def main():
    cbp = AuthenticatedClient(
        get_env(Env.COINBASE_PRO_API_KEY),
        get_env(Env.COINBASE_PRO_API_SECRET),
        get_env(Env.COINBASE_PRO_API_PASSPHRASE)
    )
    portfolio_manager = PortfolioManager(cbp)
    prediction_service = PredictionService(cbp)
    symbols_to_hold: List[str] = [x['symbol'] for x in prediction_service.get_top_currencies()]
    portfolio_manager.set_portfolio_holdings(symbols_to_hold)


if __name__ == '__main__':
    main()
