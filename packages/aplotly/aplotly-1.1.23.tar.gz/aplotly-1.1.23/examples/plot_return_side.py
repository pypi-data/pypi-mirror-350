import pandas as pd
from aplotly.plots import plot_benchmark_portfolio_returns
from aplotly import save_figure

# Load your data
df = pd.read_csv('examples/resources/monthly_report.csv', index_col='month')

# Create a plot for positive BTC months with no title
fig_positive = plot_benchmark_portfolio_returns(
    benchmark_returns=df['BTC/USDT-PERP_return'],
    portfolio_returns=df['Portfolio_return'],
    positive_months=True
)

# Create a plot for negative BTC months with a custom title
fig_negative = plot_benchmark_portfolio_returns(
    benchmark_returns=df['BTC/USDT-PERP_return'],
    portfolio_returns=df['Portfolio_return'],
    positive_months=False,
)

save_figure(fig_positive, "positive_btc_months.png")
save_figure(fig_negative, "negative_btc_months.png")

