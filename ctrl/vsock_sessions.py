from time import sleep
from threading import Thread
from random import random, randrange
from util.time import unix_time_ms
from ctrl.sessions import Sessions


class VSockSessions(Sessions):
    def __init__(self, logger=None, num_threads=2):
        super().__init__(logger)
        self._socket = VSocket(num_threads)

    def start(self):
        assert self._board_manager is not None, "Board manager must be set before starting sessions"
        try:
            self._log("Initializing bluetooth server socket...")
            spawner_thread = Thread(target=self._spawner)
            spawner_thread.start()
            self._log("Bluetooth server is listening on RFCOMM channel 1")
        except Exception as e:
            self._log(f"[Error] while starting socket {e}")


class VSocket:
    def __init__(self, num_threads):
        self._num_threads = num_threads
        self._idx = 0

    def accept(self):
        if self._idx >= self._num_threads:
            return None, None
        address = f"test-socket_{self._idx}"
        self._idx += 1
        period = 500
        return VClientSocket(address, period), (address, 0)

    def close(self):
        pass


class VClientSocket:
    def __init__(self, address, period_ms):
        self._address = address
        self._period_ms = period_ms

        """
            The following parameters are for generating random data
        """
        self._num_data_sources = 4
        self._data_difference_ratio = 0.1
        self._max_data_value = 100

        self._data = self._init_data(self._max_data_value)

    def send(self, _):
        pass

    def recv(self, _):
        data = f"t:{unix_time_ms()}" + "/"
        data += self._data_to_string()
        self._update_data()
        sleep(self._period_ms / 1000)
        return data.encode('utf-8')

    def close(self):
        pass

    def _init_data(self, scale):
        return [randrange(scale) for _ in range(self._num_data_sources)]

    def _update_data(self):
        for i in range(self._num_data_sources):
            self._data[i] += self._data_difference_ratio * self._max_data_value * (random() - 0.5)
            if self._data[i] < 0:
                self._data[i] = 0
            elif self._data[i] > self._max_data_value:
                self._data[i] = self._max_data_value

    def _data_to_string(self):
        _str = ""
        for i in range(self._num_data_sources):
            _str += f"{i}:{self._data[i]}/"
        return _str