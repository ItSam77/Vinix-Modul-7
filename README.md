# Auto MPG Dashboard 🚗

An interactive Panel-based dashboard for visualizing automobile fuel efficiency data.

## Features

- **Interactive Filters**: Filter by origin, model year, and number of cylinders
- **Multiple Visualizations**:
  - MPG vs Weight scatter plot (colored by horsepower)
  - MPG distribution histogram
  - Average MPG by origin comparison
  - Time series of MPG trends
  - MPG by cylinders analysis
  - MPG vs Horsepower by origin
- **Summary Statistics**: Quick overview of key metrics
- **Data Table**: Interactive table with filtered data
- **Responsive Design**: Beautiful, modern UI

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Dashboard

Run the Panel server with:

```bash
panel serve app.py --show
```

This will:
- Start a local server (typically at http://localhost:5006)
- Automatically open the dashboard in your browser

### Alternative run options:

**Development mode with auto-reload:**
```bash
panel serve app.py --show --autoreload
```

**Custom port:**
```bash
panel serve app.py --show --port 8080
```

**Allow external access:**
```bash
panel serve app.py --show --allow-websocket-origin=*
```

## Usage

1. Use the sidebar filters to explore the data:
   - **Select Origin**: Filter by USA, Europe, or Japan
   - **Model Year**: Adjust the year range slider
   - **Cylinders**: Select specific cylinder counts

2. Explore the visualizations tab to see relationships and trends

3. Check the data table tab to view the filtered dataset

## Dataset

The Auto MPG dataset contains information about:
- Fuel efficiency (MPG)
- Engine specifications (cylinders, horsepower, displacement)
- Vehicle characteristics (weight, acceleration)
- Manufacturing details (model year, origin)
- Car names

## Technologies Used

- **Panel**: Interactive dashboards
- **hvPlot**: High-level plotting interface
- **Pandas**: Data manipulation
- **Bokeh**: Interactive visualizations

