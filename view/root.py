import random

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20_20 as Palette

from model.board import Board
from view.plot import Plot


class Root:
    def __init__(self, doc, logger=None):
        self._data_sources = {}
        self._doc = doc
        if logger is not None:
            self._log = logger
        else:
            self._log = lambda x: print(x)
        self._plot = Plot(self._log)
        doc.add_root(self._plot.get())

    def add_board(self, board: Board):
        for source_name, source in board.get_data_sources().items():
            self._add_data_source(source_name, source)

    def _add_data_source(self, name: str, data_source: ColumnDataSource):
        assert name not in self._data_sources.keys(), f"[VIEW] Data source {name} already exists"
        self._data_sources[name] = data_source
        color = random.choice(Palette)

        def modify_doc():
            print(f"[VIEW] Adding line from source: {name}")
            line = self._figure.line(
                x="datetime", y="value",
                line_color=color, line_width=2,
                source=data_source, legend_label=name
            )
        self._doc.add_next_tick_callback(modify_doc)
