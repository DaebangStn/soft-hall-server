from abc import abstractmethod
from typing import List, Tuple


class DataFilter:
    @abstractmethod
    def filter(self, data: List[List[str]]) -> Tuple[str, str]:
        pass