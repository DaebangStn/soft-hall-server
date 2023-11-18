import random
from bokeh.models import ColumnDataSource, Button, Div, PreText, Select, CDSView, GroupFilter, CheckboxGroup
from bokeh.layouts import column, row
from bokeh.plotting import figure, curdoc
from datetime import datetime

# Data sources for each producer
data_sources = {
    "producer1": ColumnDataSource(data={"Value": [], "DateTime": [], "names": []}),
    "producer2": ColumnDataSource(data={"Value": [], "DateTime": [], "names": []}),
    "producer3": ColumnDataSource(data={"Value": [], "DateTime": [], "names": []}),
    "producer4": ColumnDataSource(data={"Value": [], "DateTime": [], "names": []})
}

# Health check indicator
# Health check indicator with fixed size
health_indicator = Div(text="""
<div style="background:green; color:white; padding:10px; width:250px; height:50px; line-height:50px; text-align:center;">
    Sensor Status: OK
</div>
""", width=250, height=50)  # Set the width and height to match the CSS for proper layout

# Log window
log_window = PreText(text="Log Messages:\n", width=500, height=200)

# Create Line Chart
fig = figure(
    x_axis_type="datetime",
    title="Data from Multiple Producers (Every Second)",
    sizing_mode="stretch_width",
    tools="pan,box_zoom,reset,save,wheel_zoom"
)

view = CDSView(source=data_sources)

colors = ["red", "green", "blue", "orange"]  # Different colors for each producer
lines = {}
for idx, (producer, data_source) in enumerate(data_sources.items()):
    lines[producer] = fig.line(
        x="DateTime", y="Value",
        line_color=colors[idx], line_width=2,
        source=data_source, legend_label=producer
    )

fig.xaxis.axis_label = "Date"
fig.yaxis.axis_label = "Random Value"
fig.legend.title = "Producers"

# Update the health check
def update_health():
    status = random.choice(["OK", "WARN", "ERROR"])
    color = {"OK": "green", "WARN": "yellow", "ERROR": "red"}[status]
    health_indicator.text = f"""<div style="background:{color};color:white;padding:10px;">Sensor Status: {status}</div>"""

# Update the log window
def log_message(new_message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_log = f"{current_time}: {new_message}\n"
    log_window.text += new_log

# Define Callbacks for updating data sources
def update_chart():
    for producer, data_source in data_sources.items():
        new_row = {"Value": [random.randint(0, 100)], "DateTime": [datetime.now()], "names": [producer]}
        data_source.stream(new_row, rollover=200)

def update_visibility(attr, old, new):
    # Loop through all lines
    for idx, producer in enumerate(producer_names):
        # If the checkbox for this producer is active, show the line, otherwise hide it
        lines[producer].visible = idx in checkbox_group.active

producer_names = sorted(data_sources.keys())
checkbox_group = CheckboxGroup(labels=producer_names, active=list(range(len(producer_names))))
checkbox_group.on_change('active', update_visibility)



# Button to update health check
update_health_button = Button(label="Update Health Status", button_type="success")
update_health_button.on_click(update_health)

# Button to log a new message
log_button = Button(label="Log New Message", button_type="primary", width=200, height=50)
log_button.on_click(lambda: log_message("New log entry"))

# Organize layout
# Widgets are arranged in a row at the top
widgets = row(log_window, update_health_button, log_button, health_indicator, checkbox_group)
# Log window and plot are arranged in a column
main_layout = column(fig, widgets)

# Add periodic callback to update chart and health
curdoc().add_periodic_callback(update_chart, 10)  # Update every second
curdoc().add_periodic_callback(update_health, 2000)  # Update every 2 seconds

# Add the layout to the current document
curdoc().add_root(main_layout)
