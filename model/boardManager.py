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
            return self.add_board(MAC)
        return self._boards[MAC]

    def add_board(self, MAC: str) -> Board:
        assert self._root is not None, "Root must be set before adding board"
        board = Board(MAC)
        self._boards[MAC] = board
        self._root.add_board(board)
        return board

    def flush(self):
        for board in list(self._boards.values()):
            board.pop()
