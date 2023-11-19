import random

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20_20 as Palette

from model.board import Board


class Root:
    def __init__(self, doc):
        self._data_sources = {}
        self._lines = {}
        self._figure = self._get_figure()
        self._doc = doc
        doc.add_root(self._figure)

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
            self._lines[name] = line
        self._doc.add_next_tick_callback(modify_doc)

    @staticmethod
    def _get_figure():
        fig = figure(
            title="Data from Multiple Producers (Every Second)",
            x_axis_type="datetime",
            sizing_mode="stretch_width",
            tools="pan,box_zoom,reset,save,wheel_zoom"
        )
        fig.xaxis.axis_label = "Date"
        fig.yaxis.axis_label = "Value"
        return fig
