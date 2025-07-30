from abc import ABC, abstractmethod
from typing import Optional
from javaobj import JavaObject
from ..AssetManager import AssetManager


class ModelBase(ABC):

    @staticmethod
    def required_float(value: Optional[str]) -> float:
        if not value:
            raise ValueError('Value is required')
        return float(value)

    @staticmethod
    def required_int(value: Optional[str]) -> int:
        if not value:
            raise ValueError('Value is required')
        return int(value)

    @staticmethod
    def required_str(value: Optional[str]) -> str:
        if not value:
            raise ValueError('Value is required')
        return value

    @classmethod
    @abstractmethod
    def from_javaobj(cls, o: JavaObject, asset_manager: AssetManager) -> 'ModelBase':
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_xml_dict(cls, data: dict, asset_manager: AssetManager) -> 'ModelBase':
        raise NotImplementedError
