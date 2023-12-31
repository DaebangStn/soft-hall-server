
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Legend, Label

from model.board import Board
from view.plot import Plot


class Root:
    def __init__(self, doc, logger=None):
        self._doc = doc
        if logger is not None:
            self._log = logger
        else:
            self._log = lambda x: print(x)
        self._plot = Plot(self._log)
        doc.add_root(self._plot.get())

    def add_data_source(self, data_source: ColumnDataSource, color: str):
        self._doc.add_next_tick_callback(lambda: self._plot.add_data(data_source, color))

    def add_legend(self, title, conf):
        self._plot.add_legend(title, conf)

    def show(self):
        div = self._plot.pack_layout()
        self._doc.add_root(div)
