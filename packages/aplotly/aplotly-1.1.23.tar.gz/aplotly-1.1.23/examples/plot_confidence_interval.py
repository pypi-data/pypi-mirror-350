import numpy as np
import pandas as pd

from aplotly import save_figure
from aplotly.plots import plot_confidence_intervals

fig = plot_confidence_intervals(
    [pd.Series(np.random.rand(100), index=np.arange(100)) for _ in range(100)],
    # labels=[f"Test {i}" for i in range(100)],
    xlabel="X",
    ylabel="Y",
    hist_width=0.2,
)
fig.show()
