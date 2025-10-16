"""
PINIX7 - Auto MPG Interactive Dashboard
Modul 7: Panel & hvPlot Dashboard

Dashboard interaktif untuk analisis data Auto MPG dengan:
- Minimal 3 pertanyaan analisis
- Minimal 2 widget interaktif
- Visualisasi menggunakan hvPlot
- Layout menggunakan Panel
"""


import panel as pn
import pandas as pd
import hvplot.pandas
import numpy as np

# Initialize Panel extension
pn.extension('tabulator')

# Load dataset
df = pd.read_csv('auto-mpg-new.csv')

# Data preprocessing
# Handle missing values in horsepower
df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
df['horsepower'].fillna(df['horsepower'].median(), inplace=True)

# Convert model year to actual year (70 -> 1970)
df['year'] = df['model year'] + 1900

# Map origin to country names
origin_map = {1: 'USA', 2: 'Europe', 3: 'Japan'}
df['origin_name'] = df['origin'].map(origin_map)

# ============================================================================
# INTERACTIVE WIDGETS
# ============================================================================



# Widget 2: Year Range Slider
year_slider = pn.widgets.RangeSlider(
    name='📅 Year Range',
    start=int(df['year'].min()),
    end=int(df['year'].max()),
    value=(int(df['year'].min()), int(df['year'].max())),
    step=1
)

# Widget 3: Cylinders Filter (Checkbox Group)
cylinders_filter = pn.widgets.CheckBoxGroup(
    name='⚙️ Filter by Cylinders',
    value=sorted(df['cylinders'].unique().tolist()),
    options=sorted(df['cylinders'].unique().tolist()),
    inline=False
)

# Widget 4: MPG Range Slider
mpg_slider = pn.widgets.RangeSlider(
    name='⛽ MPG Range',
    start=float(df['mpg'].min()),
    end=float(df['mpg'].max()),
    value=(float(df['mpg'].min()), float(df['mpg'].max())),
    step=1.0
)

# Reset Button
reset_button = pn.widgets.Button(name='🔄 Reset Filters', button_type='warning')

def reset_filters(event):
    """Reset all filters to default values"""
    year_slider.value = (int(df['year'].min()), int(df['year'].max()))
    cylinders_filter.value = sorted(df['cylinders'].unique().tolist())
    mpg_slider.value = (float(df['mpg'].min()), float(df['mpg'].max()))

reset_button.on_click(reset_filters)

# ============================================================================
# DATA FILTERING FUNCTION
# ============================================================================

def get_filtered_data(year_range, cylinders_val, mpg_range):
    """Filter data based on widget values"""
    filtered = df.copy()
    

    
    # Filter by year
    filtered = filtered[(filtered['year'] >= year_range[0]) & 
                       (filtered['year'] <= year_range[1])]
    
    # Filter by cylinders
    if cylinders_val:
        filtered = filtered[filtered['cylinders'].isin(cylinders_val)]
    
    # Filter by MPG
    filtered = filtered[(filtered['mpg'] >= mpg_range[0]) & 
                       (filtered['mpg'] <= mpg_range[1])]
    
    return filtered

# ============================================================================
# STATISTICS CARDS
# ============================================================================

@pn.depends(year_slider.param.value, 
            cylinders_filter.param.value, mpg_slider.param.value)
def create_stats_cards(year_range, cylinders_val, mpg_range):
    """Create dynamic statistics cards"""
    filtered = get_filtered_data(year_range, cylinders_val, mpg_range)
    
    stats = [
        {
            'icon': '📊',
            'label': 'Total Mobil',
            'value': f"{len(filtered)}",
            'color': '#667eea'
        },
        {
            'icon': '⛽',
            'label': 'Average MPG',
            'value': f"{filtered['mpg'].mean():.1f}",
            'color': '#f093fb'
        },
        {
            'icon': '🏎️',
            'label': 'Avg Horsepower',
            'value': f"{filtered['horsepower'].mean():.0f}",
            'color': '#4facfe'
        },
        {
            'icon': '⚖️',
            'label': 'Avg Weight',
            'value': f"{filtered['weight'].mean():.0f} lbs",
            'color': '#43e97b'
        },
        {
            'icon': '🏆',
            'label': 'Max MPG',
            'value': f"{filtered['mpg'].max():.1f}",
            'color': '#fa709a'
        }
    ]
    
    cards = []
    for stat in stats:
        card_html = f"""
        <div style="
            background: linear-gradient(135deg, {stat['color']}22 0%, {stat['color']}44 100%);
            border-left: 4px solid {stat['color']};
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 32px; margin-bottom: 10px;">{stat['icon']}</div>
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">{stat['label']}</div>
            <div style="font-size: 28px; font-weight: bold; color: {stat['color']};">{stat['value']}</div>
        </div>
        """
        cards.append(pn.pane.HTML(card_html, width=200))
    
    return pn.Row(*cards, sizing_mode='stretch_width')

# ============================================================================
# QUESTION 1: Distribusi MPG
# ============================================================================

@pn.depends(year_slider.param.value, 
            cylinders_filter.param.value, mpg_slider.param.value)
def plot_mpg_distribution(year_range, cylinders_val, mpg_range):
    """Q1: Bagaimana distribusi nilai MPG pada seluruh mobil?"""
    filtered = get_filtered_data(year_range, cylinders_val, mpg_range)
    
    plot = filtered.hvplot.hist(
        y='mpg',
        bins=30,
        title='📊 Q1: Distribusi Nilai MPG',
        xlabel='Miles Per Gallon (MPG)',
        ylabel='Frekuensi',
        color='#667eea',
        alpha=0.7,
        height=400,
        width=600,
        hover_cols=['mpg']
    ).opts(
        toolbar='above',
        active_tools=[]
    )
    
    return plot

# ============================================================================
# QUESTION 2: MPG vs Cylinders
# ============================================================================

@pn.depends(year_slider.param.value, 
            cylinders_filter.param.value, mpg_slider.param.value)
def plot_mpg_by_cylinders(year_range, cylinders_val, mpg_range):
    """Q2: Apakah ada perbedaan rata-rata MPG berdasarkan cylinders?"""
    filtered = get_filtered_data(year_range, cylinders_val, mpg_range)
    
    # Calculate average MPG by cylinders
    avg_mpg = filtered.groupby('cylinders')['mpg'].mean().reset_index()
    avg_mpg = avg_mpg.sort_values('cylinders')
    
    plot = avg_mpg.hvplot.bar(
        x='cylinders',
        y='mpg',
        title='⚙️ Q2: Rata-rata MPG Berdasarkan Jumlah Cylinders',
        xlabel='Jumlah Cylinders',
        ylabel='Average MPG',
        color='#f093fb',
        height=400,
        width=600,
        hover_cols=['cylinders', 'mpg']
    ).opts(
        toolbar='above',
        xrotation=0,
        active_tools=[]
    )
    
    return plot

# ============================================================================
# QUESTION 3: Weight vs MPG
# ============================================================================

@pn.depends(year_slider.param.value, 
            cylinders_filter.param.value, mpg_slider.param.value)
def plot_weight_vs_mpg(year_range, cylinders_val, mpg_range):
    """Q3: Bagaimana hubungan antara weight dan MPG?"""
    filtered = get_filtered_data(year_range, cylinders_val, mpg_range)
    
    plot = filtered.hvplot.scatter(
        x='weight',
        y='mpg',
        c='horsepower',
        title='⚖️ Q3: Hubungan Weight dan MPG (colored by Horsepower)',
        xlabel='Weight (lbs)',
        ylabel='MPG',
        cmap='viridis',
        size=50,
        alpha=0.6,
        height=400,
        width=600,
        hover_cols=['car name', 'weight', 'mpg', 'horsepower']
    ).opts(
        toolbar='above',
        colorbar=True,
        active_tools=[]
    )
    
    return plot

# ============================================================================
# QUESTION 4: Tren MPG per Tahun
# ============================================================================

@pn.depends(year_slider.param.value, 
            cylinders_filter.param.value, mpg_slider.param.value)
def plot_mpg_trend(year_range, cylinders_val, mpg_range):
    """Q4: Bagaimana tren rata-rata MPG dari tahun ke tahun?"""
    filtered = get_filtered_data(year_range, cylinders_val, mpg_range)
    
    # Calculate average MPG by year
    avg_mpg_year = filtered.groupby('year')['mpg'].mean().reset_index()
    
    plot = avg_mpg_year.hvplot.line(
        x='year',
        y='mpg',
        title='📈 Q4: Tren Rata-rata MPG dari Tahun ke Tahun',
        xlabel='Tahun',
        ylabel='Average MPG',
        color='#4facfe',
        line_width=3,
        height=400,
        width=600,
        hover_cols=['year', 'mpg']
    ).opts(
        toolbar='above',
        active_tools=[]
    ) * avg_mpg_year.hvplot.scatter(
        x='year',
        y='mpg',
        color='#4facfe',
        size=100,
        alpha=0.6
    )
    
    return plot

# ============================================================================
# QUESTION 5: Perbandingan Origin
# ============================================================================

@pn.depends(year_slider.param.value, 
            cylinders_filter.param.value, mpg_slider.param.value)
def plot_origin_comparison(year_range, cylinders_val, mpg_range):
    """Q5: Apakah ada perbedaan karakteristik mobil berdasarkan origin?"""
    filtered = get_filtered_data(year_range, cylinders_val, mpg_range)
    
    # Average characteristics by origin
    avg_by_origin = filtered.groupby('origin_name').agg({
        'mpg': 'mean',
        'horsepower': 'mean',
        'weight': 'mean',
        'cylinders': 'mean'
    }).reset_index()
    
    plot = avg_by_origin.hvplot.bar(
        x='origin_name',
        y='mpg',
        title='🌍 Q5: Rata-rata MPG Berdasarkan Origin',
        xlabel='Origin',
        ylabel='Average MPG',
        color='#43e97b',
        height=400,
        width=600,
        hover_cols=['origin_name', 'mpg']
    ).opts(
        toolbar='above',
        xrotation=0,
        active_tools=[]
    )
    
    return plot


# ============================================================================
# DATA EXPLORER TABLE
# ============================================================================

@pn.depends(year_slider.param.value, 
            cylinders_filter.param.value, mpg_slider.param.value)
def create_data_table(year_range, cylinders_val, mpg_range):
    """Interactive data table"""
    filtered = get_filtered_data(year_range, cylinders_val, mpg_range)
    
    # Select relevant columns
    display_cols = ['car name', 'mpg', 'cylinders', 'horsepower', 
                   'weight', 'year', 'origin_name']
    table_data = filtered[display_cols].copy()
    
    # Rename columns for better display
    table_data.columns = ['Car Name', 'MPG', 'Cylinders', 'Horsepower', 
                         'Weight', 'Year', 'Origin']
    
    table = pn.widgets.Tabulator(
        table_data,
        pagination='remote',
        page_size=20,
        sizing_mode='stretch_width',
        height=600
    )
    
    return table

# ============================================================================
# LAYOUT CONSTRUCTION
# ============================================================================

# Title and description
title = pn.pane.Markdown("""
# 🚗 PINIX7 Auto MPG Dashboard

Dashboard interaktif untuk analisis data Auto MPG dengan visualisasi dinamis dan filter interaktif.

---
""", sizing_mode='stretch_width')

# Sidebar with filters
sidebar = pn.Column(
    pn.pane.Markdown("## 🎛️ Interactive Filters"),
    pn.layout.Divider(),
    year_slider,
    pn.layout.Divider(),
    pn.pane.Markdown("### ⚙️ Filter by Cylinders"),
    cylinders_filter,
    pn.layout.Divider(),
    mpg_slider,
    pn.layout.Divider(),
    reset_button,
    pn.pane.Markdown("""
    ---
    ### 💡 Tips:
    - Gunakan filter untuk eksplorasi data
    - Hover pada plot untuk detail
    - Reset untuk kembali ke default
    """),
    width=300
)

# Analysis tab
analysis_tab = pn.Column(
    pn.pane.Markdown("## 📊 Analisis Data Auto MPG"),
    create_stats_cards,
    pn.layout.Divider(),
    pn.Row(
        plot_mpg_distribution,
        plot_mpg_by_cylinders,
        sizing_mode='stretch_width'
    ),
    pn.layout.Divider(),
    pn.Row(
        plot_weight_vs_mpg,
        plot_mpg_trend,
        sizing_mode='stretch_width'
    ),
    pn.layout.Divider(),
    pn.Row(
        plot_origin_comparison,
        sizing_mode='stretch_width'
    ),
    sizing_mode='stretch_width'
)

# Data explorer tab
data_tab = pn.Column(
    pn.pane.Markdown("## 📋 Data Explorer"),
    pn.pane.Markdown("Tabel interaktif dengan fitur sorting, pagination, dan search."),
    create_data_table,
    sizing_mode='stretch_width'
)

# Main tabs
tabs = pn.Tabs(
    ('📊 Analysis Dashboard', analysis_tab),
    ('📋 Data Explorer', data_tab),
    sizing_mode='stretch_width'
)

# Main layout
main_layout = pn.Column(
    title,
    tabs,
    sizing_mode='stretch_width'
)

# ============================================================================
# TEMPLATE
# ============================================================================

template = pn.template.FastListTemplate(
    title='PINIX7 Auto MPG Dashboard',
    sidebar=[sidebar],
    main=[main_layout],
    accent_base_color='#667eea',
    header_background='#667eea',
)

# Make it servable
template.servable()

# For running with `panel serve app.py`
if __name__ == '__main__':
    template.show()

