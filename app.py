import panel as pn
import pandas as pd
import hvplot.pandas
import numpy as np

# Initialize Panel extension
pn.extension('tabulator', sizing_mode='stretch_width')

# Load the data
df = pd.read_csv('auto-mpg.csv')

# Clean the data - handle missing horsepower values
df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
df = df.dropna(subset=['horsepower'])

# Add origin labels
origin_map = {1: 'USA', 2: 'Europe', 3: 'Japan'}
df['origin_name'] = df['origin'].map(origin_map)

# Create title
title = pn.pane.Markdown("""
# 🚗 Auto MPG Dashboard
### Interactive visualization of automobile fuel efficiency data
""", styles={'background-color': '#f0f0f0', 'padding': '10px', 'border-radius': '5px'})

# Summary statistics
def create_summary_stats():
    stats_html = f"""
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;'>
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;'>
            <h3 style='margin: 0; font-size: 2em;'>{len(df)}</h3>
            <p style='margin: 5px 0 0 0;'>Total Cars</p>
        </div>
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;'>
            <h3 style='margin: 0; font-size: 2em;'>{df['mpg'].mean():.1f}</h3>
            <p style='margin: 5px 0 0 0;'>Avg MPG</p>
        </div>
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;'>
            <h3 style='margin: 0; font-size: 2em;'>{df['horsepower'].mean():.0f}</h3>
            <p style='margin: 5px 0 0 0;'>Avg Horsepower</p>
        </div>
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;'>
            <h3 style='margin: 0; font-size: 2em;'>{df['weight'].mean():.0f}</h3>
            <p style='margin: 5px 0 0 0;'>Avg Weight (lbs)</p>
        </div>
    </div>
    """
    return pn.pane.HTML(stats_html)

# Interactive widgets
origin_select = pn.widgets.MultiSelect(
    name='Select Origin',
    options=['All', 'USA', 'Europe', 'Japan'],
    value=['All'],
    size=4
)

year_slider = pn.widgets.IntRangeSlider(
    name='Model Year',
    start=int(df['model year'].min()),
    end=int(df['model year'].max()),
    value=(int(df['model year'].min()), int(df['model year'].max())),
    step=1
)

cylinders_select = pn.widgets.MultiSelect(
    name='Cylinders',
    options=['All'] + sorted(df['cylinders'].unique().tolist()),
    value=['All'],
    size=5
)

# Function to filter data based on widgets
def get_filtered_data(origins, year_range, cylinders):
    filtered_df = df.copy()
    
    # Filter by year
    filtered_df = filtered_df[(filtered_df['model year'] >= year_range[0]) & 
                              (filtered_df['model year'] <= year_range[1])]
    
    # Filter by origin
    if 'All' not in origins:
        filtered_df = filtered_df[filtered_df['origin_name'].isin(origins)]
    
    # Filter by cylinders
    if 'All' not in cylinders:
        filtered_df = filtered_df[filtered_df['cylinders'].isin(cylinders)]
    
    return filtered_df

# Create interactive plots
@pn.depends(origin_select.param.value, year_slider.param.value, cylinders_select.param.value)
def create_scatter_plot(origins, year_range, cylinders):
    filtered_df = get_filtered_data(origins, year_range, cylinders)
    
    return filtered_df.hvplot.scatter(
        x='weight', y='mpg', 
        c='horsepower',
        cmap='viridis',
        size=80,
        alpha=0.7,
        title='MPG vs Weight (colored by Horsepower)',
        xlabel='Weight (lbs)',
        ylabel='MPG',
        width=600,
        height=400,
        colorbar=True
    )

@pn.depends(origin_select.param.value, year_slider.param.value, cylinders_select.param.value)
def create_mpg_distribution(origins, year_range, cylinders):
    filtered_df = get_filtered_data(origins, year_range, cylinders)
    
    return filtered_df.hvplot.hist(
        y='mpg',
        bins=30,
        title='MPG Distribution',
        ylabel='Frequency',
        xlabel='MPG',
        color='#667eea',
        width=600,
        height=400
    )

@pn.depends(origin_select.param.value, year_slider.param.value, cylinders_select.param.value)
def create_origin_comparison(origins, year_range, cylinders):
    filtered_df = get_filtered_data(origins, year_range, cylinders)
    
    avg_by_origin = filtered_df.groupby('origin_name')['mpg'].mean().reset_index()
    
    return avg_by_origin.hvplot.bar(
        x='origin_name',
        y='mpg',
        title='Average MPG by Origin',
        xlabel='Origin',
        ylabel='Average MPG',
        color='origin_name',
        cmap='Category10',
        width=600,
        height=400,
        legend=False,
        rot=45
    )

@pn.depends(origin_select.param.value, year_slider.param.value, cylinders_select.param.value)
def create_time_series(origins, year_range, cylinders):
    filtered_df = get_filtered_data(origins, year_range, cylinders)
    
    # Convert model year to actual year (70 = 1970, 82 = 1982)
    filtered_df['year'] = filtered_df['model year'].apply(lambda x: 1900 + x if x > 50 else 2000 + x)
    
    avg_by_year = filtered_df.groupby('year')['mpg'].mean().reset_index()
    
    return avg_by_year.hvplot.line(
        x='year',
        y='mpg',
        title='Average MPG Over Time',
        xlabel='Year',
        ylabel='Average MPG',
        color='#f5576c',
        line_width=3,
        width=600,
        height=400
    )

@pn.depends(origin_select.param.value, year_slider.param.value, cylinders_select.param.value)
def create_cylinders_plot(origins, year_range, cylinders):
    filtered_df = get_filtered_data(origins, year_range, cylinders)
    
    avg_by_cyl = filtered_df.groupby('cylinders')['mpg'].mean().reset_index()
    
    return avg_by_cyl.hvplot.bar(
        x='cylinders',
        y='mpg',
        title='Average MPG by Cylinders',
        xlabel='Number of Cylinders',
        ylabel='Average MPG',
        color='#43e97b',
        width=600,
        height=400
    )

@pn.depends(origin_select.param.value, year_slider.param.value, cylinders_select.param.value)
def create_horsepower_mpg_scatter(origins, year_range, cylinders):
    filtered_df = get_filtered_data(origins, year_range, cylinders)
    
    return filtered_df.hvplot.scatter(
        x='horsepower',
        y='mpg',
        by='origin_name',
        title='MPG vs Horsepower by Origin',
        xlabel='Horsepower',
        ylabel='MPG',
        width=600,
        height=400,
        alpha=0.6,
        size=60
    )

# Data table
@pn.depends(origin_select.param.value, year_slider.param.value, cylinders_select.param.value)
def create_data_table(origins, year_range, cylinders):
    filtered_df = get_filtered_data(origins, year_range, cylinders)
    
    # Select relevant columns and format
    display_df = filtered_df[['car name', 'mpg', 'cylinders', 'horsepower', 'weight', 'model year', 'origin_name']].copy()
    display_df.columns = ['Car Name', 'MPG', 'Cylinders', 'Horsepower', 'Weight', 'Year', 'Origin']
    
    return pn.widgets.Tabulator(
        display_df,
        page_size=10,
        pagination='remote',
        sizing_mode='stretch_width'
    )

# Create layout
controls = pn.Column(
    pn.pane.Markdown("## 🎛️ Filters", styles={'background-color': '#f8f9fa', 'padding': '10px', 'border-radius': '5px'}),
    origin_select,
    year_slider,
    cylinders_select,
    width=250,
    styles={'background-color': '#ffffff', 'padding': '15px', 'border-radius': '10px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'}
)

# Main content with tabs
plots_tab = pn.Column(
    pn.Row(create_scatter_plot, create_mpg_distribution),
    pn.Row(create_origin_comparison, create_time_series),
    pn.Row(create_cylinders_plot, create_horsepower_mpg_scatter),
)

data_tab = pn.Column(
    pn.pane.Markdown("### 📊 Filtered Data Table"),
    create_data_table
)

tabs = pn.Tabs(
    ('📈 Visualizations', plots_tab),
    ('📋 Data Table', data_tab),
    dynamic=True
)

main_content = pn.Column(
    create_summary_stats(),
    tabs
)

# Final template
template = pn.template.FastListTemplate(
    title='Auto MPG Dashboard',
    sidebar=[controls],
    main=[title, main_content],
    accent_base_color='#667eea',
    header_background='#667eea',
)

# Make it servable
template.servable()

