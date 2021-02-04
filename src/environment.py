from abc import ABC, abstractmethod

from dotenv import load_dotenv
from os import environ

load_dotenv()


class AbstractEnvironment(ABC):

    @abstractmethod
    def get_coinbase_api_key(self) -> str:
        pass

    @abstractmethod
    def get_coinbase_api_secret(self) -> str:
        pass

    @abstractmethod
    def get_coinbase_api_passphrase(self) -> str:
        pass

    @abstractmethod
    def get_n_to_hold(self) -> int:
        pass


class Environment(AbstractEnvironment):

    def get_coinbase_api_key(self) -> str:
        return environ.get('COINBASE_PRO_API_KEY')

    def get_coinbase_api_secret(self) -> str:
        return environ.get('COINBASE_PRO_API_SECRET')

    def get_coinbase_api_passphrase(self) -> str:
        return environ.get('COINBASE_PRO_API_PASSPHRASE')

    def get_n_to_hold(self) -> int:
        return int(environ.get('N_TO_HOLD'))
