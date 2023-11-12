import queue


class SensorControlQueue:
    def __init__(self):
        self.queue = queue.Queue()
