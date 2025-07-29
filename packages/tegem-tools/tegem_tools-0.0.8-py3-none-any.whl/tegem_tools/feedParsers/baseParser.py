from typing import Any
from abc import abstractmethod, ABC



class BaseParser(ABC):

    @abstractmethod
    async def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass