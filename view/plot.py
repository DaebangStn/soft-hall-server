from datetime import datetime, timedelta
from bokeh.models import ColumnDataSource, Range1d, Div, CustomJS, TextInput, Button
from bokeh.plotting import figure
from bokeh.layouts import column, row


class Plot:
    def __init__(self, logger):
        self._fig = self._init_fig()
        self._log = logger
        self._legends = []
        self._plots = set()

    def add_data(self, board_name, source_name, data_source: ColumnDataSource, color: str):
        self._plots.add((board_name, source_name))
        return self._fig.line(
            x="datetime", y="value",
            line_color=color, line_width=2,
            source=data_source,
            name=f"{board_name}-{source_name}-plot",
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
        toggle_button = Button(label="Toggle visibility", button_type="success")
        vis_off_button = Button(label="All visibility off", button_type="danger")
        vis_on_button = Button(label="All visibility on", button_type="primary")
        toggle_callback = self._toggle_visibility_callback(board_name, source_name)
        vis_off_callback = self._vis_off_callback()
        vis_on_callback = self._vis_on_callback()
        def toggle_button_logger():
            self._log(f"[VIEW] Toggled visibility for board: {board_name.value}, "
                      f"source: {source_name.value}")
        toggle_button.on_click(toggle_button_logger)
        toggle_button.js_on_click(toggle_callback)
        vis_off_button.js_on_click(vis_off_callback)
        vis_on_button.js_on_click(vis_on_callback)
        inputs = column(board_name, source_name)
        buttons = column(toggle_button, vis_off_button, vis_on_button)
        return row(inputs, buttons)

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
                    var nn_plot = nn + "-plot";
                    var plot = Bokeh.documents[0].get_model_by_name(nn_plot);
                    if (plot != null) {
                        plot.visible = !plot.visible;
                    } else {
                        console.error("Plot not found: " + nn_plot);
                    }
                });
            });
        """)

    @staticmethod
    def _vis_off_callback():
        return CustomJS(args=dict(), code=
        """
            var models = Bokeh.documents[0]._all_models.values();
            for (const m of models) {
                if (m.name && m.name.endsWith("-plot")) {
                    m.visible = false;
                }
            }
        """)

    @staticmethod
    def _vis_on_callback():
        return CustomJS(args=dict(), code=
        """
            var models = Bokeh.documents[0]._all_models.values();
            for (const m of models) {
                if (m.name && m.name.endsWith("-plot")) {
                    m.visible = true;
                }
            }
        """)
