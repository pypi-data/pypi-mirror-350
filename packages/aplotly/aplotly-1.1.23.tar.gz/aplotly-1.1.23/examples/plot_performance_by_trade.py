import numpy as np
import pandas as pd

from aplotly.plots import plot_performance_by_trade
from aplotly import save_figure

df = pd.read_csv("examples/resources/pbt.csv")

fig = plot_performance_by_trade(
    pbt=df,
)
save_figure(fig, "performance_by_trade.png", figsize=(1000, 1000))
