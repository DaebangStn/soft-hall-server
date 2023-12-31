import random

from bokeh.palettes import Category20_20 as Palette
from model.board import Board


class BoardManager:
    def __init__(self):
        self._boards = {}
        self._root = None

    def set_root(self, root):
        assert self._root is None, "Root can't set twice"
        self._root = root

    def get_board(self, MAC: str) -> Board:
        if MAC not in self._boards.keys():
            raise Exception(f"Board {MAC} not found")
            # return self.add_board(MAC)  # view cannot add board dynamically
        return self._boards[MAC]

    def add_board(self, MAC: str) -> Board:
        assert self._root is not None, "Root must be set before adding board"
        board = Board(MAC)
        self._boards[MAC] = board
        self._add_board_to_root(board)
        return board

    def flush(self):
        for board in list(self._boards.values()):
            board.pop()

    def _add_board_to_root(self, board: Board):
        conf = {}
        board_name = board.get_name()
        for source_name, source in board.get_data_sources().items():
            color = random.choice(Palette)
            self._root.add_data_source(board_name, source_name, source, color)
            conf[source_name] = color
        self._root.add_legend(board_name, conf)