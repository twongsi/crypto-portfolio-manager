from src.environment import AbstractEnvironment


class FakeEnvironment(AbstractEnvironment):

    def __init__(self, n_to_hold: int, email: str):
        self.__n_to_hold = n_to_hold
        self.__email = email

    def get_coinbase_api_key(self) -> str:
        pass

    def get_coinbase_api_secret(self) -> str:
        pass

    def get_coinbase_api_passphrase(self) -> str:
        pass

    def get_n_to_hold(self) -> int:
        return self.__n_to_hold

    def get_email(self) -> str:
        return self.__email
