import requests
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from aplotly.style import configure_plotly
import numpy as np
from aplotly import save_figure


def fetch_data(symbol: str, start: str = '2020-01-01', end: str = '2025-12-31'):
    """Fetch price data from Yahoo Finance."""
    data = yf.download(symbol, start=start, end=end)
    data.columns = data.columns.get_level_values(0)
    data.columns.name = None
    data.reset_index(inplace=True)
    data['symbol'] = symbol
    return data


def calculate_mad(series, window=90):
    """Calculate Median Absolute Deviation (MAD)."""
    # Calculate the rolling median
    rolling_median = series.rolling(window=window).median()
    # Calculate absolute deviations from the median
    abs_deviations = (series - rolling_median) / series.std()
    return abs_deviations


# ===== DATA FETCHING AND PROCESSING =====

# Fetch volatility index data from Deribit
url = "https://test.deribit.com/api/v2/public/get_volatility_index_data"
params = {
    "currency": "BTC",
    "start_timestamp": 0,
    "end_timestamp": 2099376800000,
    "resolution": "1D"
}
headers = {"Content-Type": "application/json"}

response = requests.get(url, params=params, headers=headers)
response.raise_for_status()

# Process volatility data
df = pd.DataFrame(response.json()['result']['data'], 
                 columns=['timestamp', 'open', 'high', 'low', 'close']).set_index('timestamp')
df.index = pd.to_datetime(df.index, unit='ms')

# Fetch and process price data
price_data = fetch_data('BTC-USD').set_index('Date')['Close']
price_data = calculate_mad(price_data)
price_data = price_data.resample("1W").last()

# Align data
shared_indices = price_data.index.intersection(df.index)
df = df.loc[shared_indices]
price_data = price_data.loc[shared_indices]

# ===== EVENT MARKERS =====

# Define event dates
event_dates = {
    'FTX Crisis': '2022-11-13',
    'Dollar Yen Crash': '2024-08-04',
    'US Tariffs': '2025-04-06',
    'Bybit Hack': '2025-02-21'
}

# Process event data
event_data = {}
for event_name, date_str in event_dates.items():
    event_date = pd.Timestamp(date_str)
    closest_date = df.index[df.index.get_indexer([event_date], method='nearest')[0]]
    event_data[event_name] = {
        'date': closest_date,
        'volatility': df.loc[closest_date, 'close'],
        'return': price_data.loc[closest_date]
    }

# Get the most recent data point
most_recent_volatility = df['close'].iloc[-1]
most_recent_return = price_data.iloc[-1]
event_data['Current'] = {
    'volatility': most_recent_volatility,
    'return': most_recent_return
}

# Filter data to remove anything before the first week of FTX
ftx_date = event_data['FTX Crisis']['date']
df = df[df.index >= ftx_date]
price_data = price_data[price_data.index >= ftx_date]

# ===== PLOT CREATION =====

# Configure plotly style
configure_plotly(subplots=1, color_palette="")

# Create scatter plot
fig = go.Figure()

# Add main scatter plot
fig.add_trace(
    go.Scatter(
        y=np.log10(df['close']),
        x=price_data,
        mode='markers',
        marker=dict(
            size=6,
            color='grey',
            opacity=0.7
        ),
        showlegend=False
    )
)

# Prepare marker data
marker_x = [event_data[event]['volatility'] for event in event_data]
marker_y = [event_data[event]['return'] for event in event_data]
marker_text = list(event_data.keys())
marker_colors = ['orange'] * (len(event_data) - 1) + ['red']  # All orange except the last one (Current)
marker_symbols = ['diamond'] * (len(event_data) - 1) + ['star']  # All diamond except the last one (Current)

# Add markers
fig.add_trace(
    go.Scatter(
        y=np.log10(marker_x),
        x=marker_y,
        mode='markers',
        marker=dict(
            size=8,
            color=marker_colors,
            symbol=marker_symbols
        ),
        showlegend=False
    )
)

# ===== AXIS SETUP =====

# Calculate y-axis values
y_min = np.log10(df['close'].min())
y_max = np.log10(df['close'].max())
y_range = y_max - y_min
avg_y = np.log10(df['close'].mean())

# Calculate x-axis values
x_min = -max(abs(price_data.min()), abs(price_data.max()))
x_max = max(abs(price_data.min()), abs(price_data.max()))
x_extent = x_max - x_min

# Center y-axis on mean
max_distance_from_mean = max(abs(y_max - avg_y), abs(y_min - avg_y))
y_min_adjusted = avg_y - max_distance_from_mean
y_max_adjusted = avg_y + max_distance_from_mean
y_range_adjusted = y_max_adjusted - y_min_adjusted

# Plot dimensions and padding
plot_width = 1170
plot_height = 650
pixel_padding = 5
x_padding = (x_max - x_min) * (pixel_padding / plot_width)
y_padding = (y_max_adjusted - y_min_adjusted) * (pixel_padding / plot_height)

# ===== SHAPES AND LINES =====

# Add vertical line at x=0
fig.add_shape(
    type="line",
    x0=0,
    y0=y_min_adjusted - y_padding,
    x1=0,
    y1=y_max_adjusted + y_padding,
    line=dict(
        color="black",
        width=1,
        dash="solid",
    ),
)

# Add horizontal line at average y value
fig.add_shape(
    type="line",
    x0=x_min - x_padding,
    y0=avg_y,
    x1=x_max + x_padding,
    y1=avg_y,
    line=dict(
        color="black",
        width=1,
        dash="solid",
    ),
)

# ===== ANNOTATIONS =====

# Create annotations for event markers
annotations = []
for i, (x, y, text) in enumerate(zip(marker_x, marker_y, marker_text)):
    color = marker_colors[i]
    annotations.append(
        dict(
            x=y,
            y=np.log10(x) + (np.log10(max(marker_x)) - np.log10(min(marker_x))) * 0.1,
            text=text,
            showarrow=False,
            font=dict(
                size=12,
                color=color
            ),
            bgcolor="white",
            opacity=0.8,
            bordercolor="black",
            borderwidth=0,
            borderpad=4,
            ax=0,
            ay=-30
        )
    )

# Add axis label annotations
annotations.append(
    dict(
        x=x_min + x_extent * 0.75,  # 75% across the x-axis
        y=y_max_adjusted - y_padding * 3,  # Move to bottom
        text="Optimistic",
        showarrow=False,
        font=dict(
            size=14,
            color="white"
        ),
        bgcolor="black",
        opacity=1.0,
        bordercolor="black",
        borderwidth=0,
        borderpad=4,
        ax=0,
        ay=0
    )
)

annotations.append(
    dict(
        x=x_min + x_extent * 0.25,  # 25% across the x-axis
        y=y_max_adjusted - y_padding * 3,  # Move to bottom
        text="Pessimistic",
        showarrow=False,
        font=dict(
            size=14,
            color="white"
        ),
        bgcolor="black",
        opacity=1.0,
        bordercolor="black",
        borderwidth=0,
        borderpad=4,
        ax=0,
        ay=0
    )
)

annotations.append(
    dict(
        x=x_min + x_padding * 3,
        y=y_max_adjusted - y_range_adjusted * 0.25,  # 25% down from the top
        text="High",
        showarrow=False,
        font=dict(
            size=14,
            color="white"
        ),
        bgcolor="black",
        opacity=1.0,
        bordercolor="black",
        borderwidth=0,
        borderpad=4,
        ax=-30,
        ay=0,
        textangle=270  # Rotate by 270 degrees
    )
)

annotations.append(
    dict(
        x=x_min + x_padding * 3,
        y=y_max_adjusted - y_range_adjusted * 0.75,  # 75% down from the top
        text="Low",
        showarrow=False,
        font=dict(
            size=14,
            color="white"
        ),
        bgcolor="black",
        opacity=1.0,
        bordercolor="black",
        borderwidth=0,
        borderpad=4,
        ax=-30,
        ay=0,
        textangle=270  # Rotate by 270 degrees
    )
)

# ===== LAYOUT AND STYLING =====

# Update layout with annotations
fig.update_layout(
    yaxis_title='Uncertainty',
    xaxis_title='Sentiment',
    showlegend=False,
    annotations=annotations,
    xaxis=dict(
        range=[x_min - x_padding, x_max + x_padding],
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        tickwidth=0,
        ticklen=0,
        title=dict(
            text='Sentiment',
            standoff=10,
            font=dict(size=14)
        )
    ),
    yaxis=dict(
        range=[y_max_adjusted + y_padding, y_min_adjusted - y_padding],  # Flipped y-axis range
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        tickwidth=0,
        ticklen=0,
        title=dict(
            text='Uncertainty',
            standoff=10,
            font=dict(size=14)
        )
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='white',
    margin=dict(l=30, r=30, t=30, b=30),
    width=plot_width,
    height=plot_height
)

# ===== GRADIENT BACKGROUND =====

# Add a gradient background
fig.add_shape(
    type="rect",
    x0=x_min - x_padding,
    y0=y_min_adjusted - y_padding,
    x1=x_max + x_padding,
    y1=y_max_adjusted + y_padding,
    fillcolor="rgba(0,0,0,0)",
    line=dict(width=0),
    layer="below"
)

# Add gradient background using multiple rectangles
num_gradients = 50
for i in range(num_gradients):
    # Calculate position for this gradient segment
    x_start = (x_min - x_padding) + ((x_max + x_padding) - (x_min - x_padding)) * i / num_gradients
    x_end = (x_min - x_padding) + ((x_max + x_padding) - (x_min - x_padding)) * (i + 1) / num_gradients
    
    # Calculate color for this segment (orange to blue)
    r = 1 - i / num_gradients  # Red component (1 to 0)
    g = 0.65 - 0.65 * i / num_gradients  # Green component (0.65 to 0) - reduced for orange
    b = i / num_gradients      # Blue component (0 to 1)
    
    fig.add_shape(
        type="rect",
        x0=x_start,
        y0=y_min_adjusted - y_padding,
        x1=x_end,
        y1=y_max_adjusted + y_padding,
        fillcolor=f"rgba({int(r*255)},{int(g*255)},{int(b*255)},0.3)",
        line=dict(width=0),
        layer="below"
    )

# Show the plot
save_figure(fig, "market.png")