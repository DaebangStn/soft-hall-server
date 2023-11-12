import queue


class SensorDataQueue:
    def __init__(self):
        self.queue = queue.Queue()
