from dotenv import load_dotenv
from os import environ

load_dotenv()


def get_coinbase_api_key() -> str:
    return environ.get('COINBASE_PRO_API_KEY')


def get_coinbase_api_secret() -> str:
    return environ.get('COINBASE_PRO_API_SECRET')


def get_coinbase_api_passphrase() -> str:
    return environ.get('COINBASE_PRO_API_PASSPHRASE')
