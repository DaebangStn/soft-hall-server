from abc import abstractmethod
from typing import List, Tuple, Optional

from util.time import cvt_unix_time_ms_to_datetime


class DataFilter:
    @abstractmethod
    def filter(self, data: List[List[str]]) -> Tuple[str, str]:
        """
        :param data:
            list of [source_name, value]
        :return:
            (timestamp, value)
            if value is None, then the data is invalid
        """
        pass

    @property
    def __name__(self):
        return self.__class__.__name__


class MeanFilter(DataFilter):
    def filter(self, data: List[List[str]]) -> Tuple[str, Optional[str]]:
        """
        :param data:
            list of [source_name, value]
        :return:
            (timestamp, value)
            if value is None, then the data is invalid
        """
        values = []
        stamp = None
        for d in data:
            if d[0] == 't':
                stamp = cvt_unix_time_ms_to_datetime(int(d[1]))
            else:
                values.append(float(d[1]))
        if len(values) == 0:
            return stamp, None
        val = sum(values) / len(values)
        return stamp, str(val)

    @property
    def __name__(self):
        return "m"


class MovingAverageFilter(DataFilter):
    def __init__(self, source_name:str, window_size: int = 5):
        self._source_name = source_name
        self._window_size = window_size
        self._window = []

    def filter(self, data: List[List[str]]) -> Tuple[str, Optional[str]]:
        """
        :param data:
            list of [source_name, value]
        :return:
            (timestamp, value)
            if value is None, then the data is invalid
        """
        stamp = None
        for d in data:
            if d[0] == 't':
                stamp = cvt_unix_time_ms_to_datetime(int(d[1]))
            elif d[0] == self._source_name:
                self._append(float(d[1]))
        if len(self._window) < self._window_size:
            return stamp, None
        val = sum(self._window) / len(self._window)
        return stamp, str(val)

    def _append(self, value: float):
        self._window.append(value)
        if len(self._window) > self._window_size:
            self._window.pop(0)


    @property
    def __name__(self):
        return f"ma{self._source_name}_{self._window_size}"