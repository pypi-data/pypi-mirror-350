from functools import wraps
from typing import Any, Callable, TypeVar

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger

LOG = get_logger()

T = TypeVar("T")


def repository_class(cls: T) -> T:
    for attr_name in cls.__dict__.keys():
        attr = getattr(cls, attr_name)

        if callable(attr):
            setattr(cls, attr_name, _repository_method(attr))

    return cls


def _repository_method(method: Callable[..., Any]) -> Callable:
    @wraps(method)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return method(*args, **kwargs)
        except ApplicationException as e:
            raise e
        except Exception as e:
            LOG.error(f"An internal server error occurred: {e}")
            raise ApplicationException(
                Exceptions.InternalServerException,
                "An internal server error occurred.",
                ["An internal server error occurred."],
            )

    return wrapper
