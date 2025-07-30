from typing import Generic, TypeVar

import jwt
from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.utils.jwt import ABCJwtHandler

LOG = get_logger()

Payload = TypeVar("Payload", bound=dict)


class JwtHandler(Generic[Payload], ABCJwtHandler[Payload]):
    def __init__(self, secret: str, algorithm: str) -> None:
        self._secret = secret
        self._algorithm = algorithm

    def encode(self, payload: Payload) -> str:
        try:
            return jwt.encode(
                dict(payload),
                self._secret,
                algorithm=self._algorithm,
            )
        except Exception as e:
            LOG.error(f"Error encoding jwt payload: {e}")
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Internal server error.",
                ["Internal server error."],
            ) from e

    def decode(self, token: str) -> Payload:
        try:
            return jwt.decode(
                token,
                self._secret,
                algorithms=[self._algorithm],
            )
        except Exception as e:
            LOG.error(f"Error decoding jwt token: {e}")
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Token validation failed.",
                ["Token is malformed."],
            ) from e
