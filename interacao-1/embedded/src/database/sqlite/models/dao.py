from abc import ABC, abstractmethod
from typing import Any

class DAO(ABC):
    @abstractmethod
    def find_one(self, where: dict) -> tuple:
        pass

    @abstractmethod
    def find_all(self, where: dict) -> tuple:
        pass
    
    @abstractmethod
    def create(self, data: dict, returning = '*') -> tuple:
        pass

    @abstractmethod
    def to_json(self, data: tuple) -> dict:
        pass
    
    @abstractmethod
    def to_json_list(self, data: list) -> list:
        pass