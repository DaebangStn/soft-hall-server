import socket
from threading import Thread
from model.boardManager import BoardManager
from util.config import load_config
from util.time import unix_time_us_ascii


class Sessions:
    def __init__(self, logger=None):
        self._config = load_config()['sessions']
        self._parse_config()
        self._board_manager = None
        self._socket = None
        if logger is not None:
            self._log = logger
        else:
            self._log = lambda x: print(x)

    def set_board_manager(self, board_manager: BoardManager):
        assert self._board_manager is None, "Board manager can't set twice"
        self._board_manager = board_manager

    def start(self):
        assert self._board_manager is not None, "Board manager must be set before starting sessions"
        try:
            self._socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self._log("Initializing bluetooth server socket...")
            self._socket.bind((self._adaptor_mac, 1))
            self._socket.listen(self._max_sessions)
            spawner_thread = Thread(target=self._spawner)
            spawner_thread.start()
            self._log("Bluetooth server is listening on RFCOMM channel 1")
        except Exception as e:
            self._socket.close()
            self._log(f"[Error] while starting socket {e}")

    def _parse_config(self):
        self._adaptor_mac = self._config['adaptor-mac']
        self._max_sessions = self._config['max-sessions']

    def _spawner(self):
        while True:
            client_socket = None
            try:
                client_socket, _address = self._socket.accept()
                client_address = _address[0]
                self._log(f"Accepted connection from {client_address}")
                board = self._board_manager.get_board(client_address)
                client_thread = Thread(target=self._session_handler, args=(client_socket, client_address, board))
                client_thread.start()
            except Exception as e:
                self._log(f"[Error] while spawning sessions {e}")
                if client_socket is not None:
                    client_socket.close()
                break

    def _session_handler(self, _socket, address, board):
        self._log(f"[Session] starting with {address}")
        _socket.send(unix_time_us_ascii())
        print("unix time sent", unix_time_us_ascii())
        while True:
            try:
                data = _socket.recv(300)
                if data:
                    board.push(data)
            except Exception as e:
                self._log(f"[Session] exception {e}")
                _socket.close()
                break
