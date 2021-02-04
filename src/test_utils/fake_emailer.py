from typing import Optional

from src.emailer import AbstractEmailer


class FakeEmailer(AbstractEmailer):
    def __init__(self):
        self.__to: Optional[str] = None
        self.__subject: Optional[str] = None
        self.__body: Optional[str] = None

    def send(self, to: str, subject: str, body: str) -> None:
        self.__to = to
        self.__subject = subject
        self.__body = body

    @property
    def to(self) -> Optional[str]:
        return self.__to

    @property
    def subject(self) -> Optional[str]:
        return self.__subject

    @property
    def body(self) -> Optional[str]:
        return self.__body