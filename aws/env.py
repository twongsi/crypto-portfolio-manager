import os


def env(key: str) -> str:
    return os.environ.get(key)