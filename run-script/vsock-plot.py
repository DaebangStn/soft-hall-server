from model.boardManager import BoardManager
from ctrl.vsock_sessions import VSockSessions
from view.root import Root
from bokeh.server.server import Server

num_threads = 4


def modify_doc(doc):
    root = Root(doc)
    board_manager = BoardManager()
    board_manager.set_root(root)
    for i in range(num_threads):
        board_manager.add_board(f"test-socket_{i}")
    root.show()

    sessions = VSockSessions(print, num_threads)
    sessions.set_board_manager(board_manager)
    sessions.start()

    doc.add_periodic_callback(board_manager.flush, 1000)


def run_server():
    # Define the apps as a dictionary
    apps = {'/': modify_doc}

    # Create and configure the server
    server = Server(apps, port=5006, address='0.0.0.0', allow_websocket_origin=["*"])
    server.start()

    # Start the I/O loop
    server.io_loop.start()


if __name__ == '__main__':
    run_server()
