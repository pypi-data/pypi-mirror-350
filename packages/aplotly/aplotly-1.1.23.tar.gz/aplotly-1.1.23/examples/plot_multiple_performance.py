import numpy as np
import pandas as pd

from aplotly.plots import plot_multiple_performance

fig = plot_multiple_performance(
    [pd.Series(np.random.rand(100), index=np.arange(100)) for _ in range(3)],
    [pd.Series(np.random.rand(100), index=np.arange(100)) for _ in range(3)],
    labels=["Test 1", "Test 2", "Test 3"],
    xlabel="X",
)
fig.show()
