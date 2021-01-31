from src.environment import AbstractEnvironment


class FakeEnvironment(AbstractEnvironment):

    def __init__(self, n_portfolio_holdings: int = 0):
        self.__n_portfolio_holdings = n_portfolio_holdings

    def get_coinbase_api_key(self) -> str:
        pass

    def get_coinbase_api_secret(self) -> str:
        pass

    def get_coinbase_api_passphrase(self) -> str:
        pass

    def get_n_portfolio_holdings(self) -> int:
        return self.__n_portfolio_holdings