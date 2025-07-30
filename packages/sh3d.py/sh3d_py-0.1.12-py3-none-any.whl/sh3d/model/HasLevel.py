from typing import Optional
from abc import ABC, abstractmethod
from sh3d.model.Level import Level


class HasLevel(ABC):

    @property
    @abstractmethod
    def level(self) -> Optional[Level]:
        raise NotImplementedError

    def is_at_level(self, level: Level) -> bool:
        raise NotImplementedError
