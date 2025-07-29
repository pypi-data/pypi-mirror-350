from abc import ABC, abstractmethod
from typing import List

from whiskerrag_types.model.knowledge import Knowledge


class BaseDecomposer(ABC):
    def __init__(self, knowledge: Knowledge):
        self.knowledge = knowledge

    @abstractmethod
    async def decompose(self) -> List[Knowledge]:
        pass
