from dotenv import load_dotenv
from enum import Enum
from os import environ

load_dotenv()


class Env(Enum):
    COINBASE_PRO_API_KEY = 'COINBASE_PRO_API_KEY'
    COINBASE_PRO_API_SECRET = 'COINBASE_PRO_API_SECRET'
    COINBASE_PRO_API_PASSPHRASE = 'COINBASE_PRO_API_PASSPHRASE'
    N_PORTFOLIO_HOLDINGS = 'N_PORTFOLIO_HOLDINGS'


def get_env(var: Env) -> str:
    return environ.get(var.value)
