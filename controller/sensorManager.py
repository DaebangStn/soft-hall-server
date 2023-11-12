import socket
import threading

from model.sensorDataQueue import SensorDataQueue
from model.sensorControlQueue import SensorControlQueue


class SensorManager:
    def __init__(self, server_mac, log, max_connections=10):
        self._log = log
        self._server = None
        self._data = None
        self._control = None
        self._max_connections = max_connections
        self._server_mac = server_mac

    def start(self):
        try:
            self._server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self._data = SensorDataQueue()
            self._control = SensorControlQueue()

            self._log("Initializing bluetooth server socket...")
            self._server.bind((self._server_mac, 1))
            self._server.listen(self._max_connections)
            self._log("Bluetooth server is listening on RFCOMM channel 1")
        finally:
            self._server.close()
            self._log("Bluetooth server socket closed")

    def __spawner(self, log, server_socket, data_q, control_q):
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                log(f"Accepted connection from {client_address}")
                client_thread = threading.Thread(
                    target=self.__client_handler,
                    args=(log, client_socket, client_address, data_q, control_q))
                client_thread.start()
                log(f"Started thread for {client_address}")
            except Exception as e:
                log(f"Exception: {e}")
                break

    def __client_handler(self, log, client_socket, client_address, data_q, control_q):
        pass

