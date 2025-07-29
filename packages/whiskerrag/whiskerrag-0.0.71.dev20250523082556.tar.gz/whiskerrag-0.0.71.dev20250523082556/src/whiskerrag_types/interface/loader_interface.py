from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from whiskerrag_types.model.knowledge import Knowledge
from whiskerrag_types.model.multi_modal import Image, Text

T = TypeVar("T", Image, Text)


class BaseLoader(ABC, Generic[T]):
    def __init__(self, knowledge: Knowledge):
        self.knowledge = knowledge

    @abstractmethod
    async def load(self) -> List[T]:
        pass
