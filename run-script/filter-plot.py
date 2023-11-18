from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select, CDSView, GroupFilter

# Sample data
data = dict(
    names=['producer1', 'producer2', 'producer1', 'producer3', 'producer2'],
    x=[1, 2, 3, 4, 5],
    y=[5, 4, 3, 2, 1]
)
source = ColumnDataSource(data)

# Initial view with no filters
view = CDSView(source=source)

# Create a figure
plot = figure(x_range=(0, 6), y_range=(0, 6))
plot.circle(x='x', y='y', source=source, size=15, view=view)

# Create a select widget
options = ["all"] + sorted(set(data['names']))
select_widget = Select(title="Select Producer:", value="all", options=options)

# Callback function to filter data based on the select widget
def update_plot(attr, old, new):
    if select_widget.value != 'all':  # Apply the filter
        view.filters = [GroupFilter(column_name='names', group=select_widget.value)]
    else:  # Show all data
        view.filters = []

select_widget.on_change('value', update_plot)

# Add the select widget and plot to the document
layout = column(select_widget, plot)
curdoc().add_root(layout)

# To run this script from the command line, use:
# bokeh serve --show script_name.py
