from datetime import datetime, timedelta
from bokeh.models import ColumnDataSource, Range1d, Div, CustomJS, TextInput, Button
from bokeh.plotting import figure
from bokeh.layouts import column, row


class Plot:
    def __init__(self, logger):
        self._fig = self._init_fig()
        self._log = logger
        self._legends = []
        self._plots = {}

    def add_data(self, board_name, source_name, data_source: ColumnDataSource, color: str):
        return self._fig.line(
            x="datetime", y="value",
            line_color=color, line_width=2,
            source=data_source,
            name=f"{board_name}-{source_name}",
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

    def add_visibility_input(self):
        """
            board_name: comma separated string input for board names
            source_name: comma separated string input for source names
        """
        board_name = TextInput(title="Board name:", value="")
        source_name = TextInput(title="Source name:", value="")
        button = Button(label="Toggle visibility", button_type="success")
        callback = self._toggle_visibility_callback(board_name, source_name)
        def button_logger():
            self._log(f"[VIEW] Toggled visibility for board: {board_name.value}, "
                      f"source: {source_name.value}")
        button.on_click(button_logger)
        button.js_on_click(callback)
        return column(board_name, source_name, button)

    def get(self):
        return self._fig

    def pack_layout(self):
        legend_layout = row(*self._legends, self.add_visibility_input())
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

    @staticmethod
    def _toggle_visibility_callback(board_name: TextInput, source_name: TextInput):
        return CustomJS(args=dict(
            board_name=board_name,
            source_name=source_name,
        ), code=
        """
            var n1 = board_name.value.split(",");
            n1.forEach(function(bn) {
                var n2 = source_name.value.split(",");
                n2.forEach(function(sn) {
                    var nn = bn + "-" + sn;
                    var plot = Bokeh.documents[0].get_model_by_name(nn);
                    plot.visible = !plot.visible;
                });
            });
        """)