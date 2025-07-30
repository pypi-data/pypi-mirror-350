from abc import ABC, abstractmethod


class BaseSessionManager(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def init(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def session(self):
        pass

    @abstractmethod
    async def asession(self):
        pass
