import pandas as pd
import seaborn as sns
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import Select, Slider, ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import Category10

# Load the dataset using pandas
df = pd.read_csv('bank.csv')

# Create the initial data source for the plots
source = ColumnDataSource(data=df)

# Create the scatter plot
scatter = figure(title='Scatter Plot', plot_width=400, plot_height=400)
scatter.circle(x='age', y='balance', source=source, size=8,
               color=factor_cmap('job', Category10[10], factors=df['job'].unique()))

# Create the histogram
hist = figure(title='Histogram', plot_width=400, plot_height=400)
hist.vbar(x='age_bin', top='frequency', width=0.9, source=source, fill_color='dodgerblue')

# Create the widgets
select_job = Select(title='Job', options=['All'] + list(df['job'].unique()), value='All')
slider_age_bins = Slider(title='Number of Age Bins', start=5, end=50, step=5, value=10)


# Define the update function
def update_data():
    selected_job = select_job.value
    num_age_bins = slider_age_bins.value

    # Filter the data based on the selected job
    filtered_data = df if selected_job == 'All' else df[df['job'] == selected_job]

    # Update the scatter plot
    scatter.title.text = f'Scatter Plot ({selected_job})'
    scatter.data_source.data = dict(age=filtered_data['age'], balance=filtered_data['balance'],
                                    job=filtered_data['job'])

    # Update the histogram
    hist.title.text = f'Age Histogram ({selected_job})'
    hist_data, hist_edges = np.histogram(filtered_data['age'], bins=num_age_bins)
    hist.data_source.data = dict(age_bin=hist_edges[:-1], frequency=hist_data)


# Update the data when the widget values change
select_job.on_change('value', lambda attr, old, new: update_data())
slider_age_bins.on_change('value', lambda attr, old, new: update_data())

# Set up the layout
layout = column(row(select_job, slider_age_bins), row(scatter, hist))

# Call the update function to initialize the plots
update_data()

# Add the layout to the document
curdoc().add_root(layout)
