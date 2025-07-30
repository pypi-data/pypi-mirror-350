from ed_domain.utils.security.password import ABCPasswordHandler
from passlib.context import CryptContext


class PasswordHandler(ABCPasswordHandler):
    def __init__(self, scheme: str) -> None:
        self._context = CryptContext(schemes=[scheme], deprecated="auto")

    def hash(self, password: str) -> str:
        return self._context.hash(password)

    def verify(self, password: str, hash: str) -> bool:
        return self._context.verify(password, hash)
