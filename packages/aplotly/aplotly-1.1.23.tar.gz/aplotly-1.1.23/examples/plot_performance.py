import numpy as np
import pandas as pd

from aplotly.plots import plot_performance

fig = plot_performance(
    pd.Series(np.random.rand(100), index=np.arange(100)),
    pd.Series(np.random.rand(100), index=np.arange(100)),
    performance_label="Test",
    drawdown_label="Test",
    xlabel="X",
)
fig.show()
