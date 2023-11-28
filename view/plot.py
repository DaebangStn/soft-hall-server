from datetime import datetime, timedelta
from bokeh.models import ColumnDataSource, Range1d
from bokeh.plotting import figure


class Plot:
    def __init__(self, logger):
        self._fig = self._init_fig()
        self._log = logger

    def add_data(self, name: str, data_source: ColumnDataSource, color: str):
        self._fig.line(
            x="datetime", y="value",
            line_color=color, line_width=2,
            source=data_source, legend_label=name
        )
        # self._fig.circle(
        #     x="datetime", y="value",
        #     line_color=color, size=2,
        #     source=data_source, legend_label=name
        # )

    def get(self):
        return self._fig

    @staticmethod
    def _init_fig() -> figure:
        return figure(
            title="Soft hall tactile sensor",
            x_axis_type="datetime",
            x_axis_label="Date",
            y_axis_label="Value",
            x_range=Range1d(datetime.now() - timedelta(seconds=10), datetime.now() + timedelta(minutes=1)),
            sizing_mode="stretch_width",
            tools="pan,box_zoom,reset,save,wheel_zoom"
        )
