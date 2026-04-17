import abc
from typing import type_check_only

_DEFAULT_TIMEOUT: int = 120

@type_check_only
class _BaseAuthorizedSession(metaclass=abc.ABCMeta):
    credentials: object

    def __init__(self, credentials: object) -> None: ...
    @abc.abstractmethod
    def request(
        self,
        method: str,
        url: str,
        data: object = None,
        headers: object = None,
        max_allowed_time: object = None,
        timeout: int = ...,
        **kwargs: object,
    ) -> object: ...
    @abc.abstractmethod
    def close(self) -> None: ...
