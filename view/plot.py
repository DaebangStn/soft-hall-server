from datetime import datetime, timedelta
from bokeh.models import ColumnDataSource, Range1d, Div
from bokeh.plotting import figure, show
from bokeh.layouts import column, row


class Plot:
    def __init__(self, logger):
        self._fig = self._init_fig()
        self._log = logger
        self._legends = []

    def add_data(self, data_source: ColumnDataSource, color: str):
        return self._fig.line(
            x="datetime", y="value",
            line_color=color, line_width=2,
            source=data_source
        )
        # self._fig.circle(
        #     x="datetime", y="value",
        #     line_color=color, size=2,
        #     source=data_source, legend_label=name
        # )

    def add_legend(self, title: str, conf: dict):
        legend_html = '<div style="padding: 10px; background-color: white; border: 1px solid #ddd;">'
        legend_html += f'<h3>{title}</h3>'
        for name, color in conf.items():
            legend_html += f'<div><span style="color: {color};">&#11044;</span> {name}</div>'
        legend_html += '</div>'
        legend_div = Div(text=legend_html)
        self._legends.append(legend_div)

    def get(self):
        return self._fig

    def pack_layout(self):
        legend_layout = row(*self._legends)
        return legend_layout

    @staticmethod
    def _init_fig() -> figure:
        return figure(
            title="Soft hall tactile sensor",
            x_axis_type="datetime",
            x_axis_label="Date",
            y_axis_label="Value",
            x_range=Range1d(datetime.now() - timedelta(seconds=10), datetime.now() + timedelta(minutes=1)),
            sizing_mode="stretch_width",
            tools="pan,box_zoom,reset,save,wheel_zoom",
        )
