import numpy as np
import pandas as pd

from aplotly.plots import plot_multiple_lines

fig = plot_multiple_lines(
    [pd.Series(np.random.rand(100), index=np.arange(100)) for _ in range(3)],
    labels=["Test 1", "Test 2", "Test 3"],
    styles=[{"shape": "hv"}, {"shape": "vh"}, {"shape": "linear"}],
    xlabel="X",
    ylabel="Y",
    colors=["rgba(255, 0, 0, 1.0)", "rgba(0, 255, 0, 0.5)", "rgba(0, 0, 255, 0.25)"],
)
fig.show()
