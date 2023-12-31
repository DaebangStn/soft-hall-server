from typing import Dict, List, ByteString, Optional, Tuple
from queue import SimpleQueue
from model.dataFilter import DataFilter
from util.config import load_config
from util.path import get_log_file_path
from util.time import timestamp, unix_time_ms, cvt_unix_time_ms_to_datetime
from bokeh.models import ColumnDataSource


class Board:
    def __init__(self, MAC, logger=None):
        self._MAC = MAC
        self._config = load_config()['board']
        self._name = None
        self._rollover = None
        self._parse_config()
        self._log_file = self._get_log()
        self._q = SimpleQueue()
        self._sources = {}
        self._filters = []
        self._add_sources('0')  # Must match the third character in the payload
        self._add_sources('1')  # Must match the third character in the payload
        self._add_sources('2')  # Must match the third character in the payload
        self._add_sources('3')  # Must match the third character in the payload
        if logger is not None:
            self._logger = logger
        else:
            self._logger = lambda x: print(x)

    def push(self, data):
        self._q.put(data)

    def get_name(self):
        return self._name

    def get_item_num(self):
        return self._q.qsize()

    def get_data_sources(self):
        return self._sources

    def add_filter(self, _filter: DataFilter):
        self._filters.append(_filter)
        self._add_sources(_filter.__name__)

    def pop(self, num_pop=None):
        total_data = {}  # {source_name: ([values], [times])}
        if num_pop is None:
            num_pop = self._q.qsize()
        for _ in range(num_pop):
            if self._q.empty():
                break
            raw_bin = self._q.get()
            raw_serialized = self._deserialize(raw_bin)
            if raw_serialized is None:
                continue
            raw_valid = self._extract_valid(raw_serialized)
            # To inspect data, self._log(f"{self._data_valid_to_str(raw_valid)}")
            self._append_raw_data(total_data, raw_valid)
            self._append_filtered(total_data, raw_valid)

        self._log(f"streaming {len(total_data)} sources")
        for source_name, (values, times) in total_data.items():
            self._sources[source_name].stream({'value': values, 'datetime': times}, self._rollover)

    def _add_sources(self, source_name):
        self._sources[source_name] = ColumnDataSource(data={'value': [], 'datetime': []})

    def _append_filtered(self, total_data: Dict[str, Tuple[List[int], List[int]]], data_valid: List[List[str]]):
        for _filter in self._filters:
            stamp, value = _filter.filter(data_valid)
            if value is None:
                continue
            source_name = _filter.__name__
            if source_name not in total_data.keys():
                total_data[source_name] = ([value], [stamp])
            else:
                total_data[source_name][0].append(value)
                total_data[source_name][1].append(stamp)

    def _deserialize(self, data_bin: ByteString) -> Optional[List[List[str]]]:
        try:
            last_slash_index = data_bin.find(b'\x00')
            if last_slash_index != -1:
                data_bin = data_bin[:last_slash_index]
            data_str = data_bin.decode('utf-8').strip()
            data_row = data_str.split('/')[:-1]
            data_serialized = [row.split(':') for row in data_row]
        except Exception as e:
            self._log(f"Invalid data: {data_bin}")
            return None
        return data_serialized

    def _extract_valid(self, data_serialized: List[List[str]]) -> List[List[str]]:
        data_valid = []
        for row in data_serialized:
            if len(row) != 2:
                self._log(f"Invalid data: {row}")
                continue
            source_name = row[0]
            if source_name not in self._sources.keys():
                if source_name != 't':
                    self._log(f"Invalid source name: {source_name}")
                    continue
            data_valid.append(row)
        return data_valid

    def _parse_config(self):
        self._name = self._get_name()
        self._rollover = self._config['data-rollover']

    def _get_name(self):
        alias = self._config['mac-alias']
        if self._MAC in alias:
            return alias[self._MAC]['name']
        else:
            return self._MAC

    def _get_log(self):
        log_path = get_log_file_path(prefix=self._name)
        return open(log_path, 'w')

    def _log(self, log):
        self._logger(f"[{self._name}]{timestamp()}: {log}")
        self._log_file.write(f"{log}\n")

    def _log_line_clear(self):
        self._log_file.write("\n")
        self._logger("")

    @staticmethod
    def _append_raw_data(total_data: Dict[str, Tuple[List[int], List[int]]], data_valid: List[List[str]]):
        if data_valid[0][0] == 't':
            indices = range(1, len(data_valid))
            stamp = int(data_valid[0][1])
        else:
            indices = range(len(data_valid))
            stamp = unix_time_ms()
        dt = cvt_unix_time_ms_to_datetime(stamp)
        for i in indices:
            source_name = data_valid[i][0]
            value = float(data_valid[i][1])
            if source_name not in total_data.keys():
                total_data[source_name] = ([value], [dt])
            else:
                total_data[source_name][0].append(value)
                total_data[source_name][1].append(dt)

    @staticmethod
    def _data_valid_to_str(data: List[List[str]]) -> str:
        return '/'.join([':'.join(row) for row in data])
