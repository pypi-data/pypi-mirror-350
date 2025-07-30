import numpy as np
import pandas as pd

from aplotly import save_figure
from aplotly.plots import plot_line

fig = plot_line(
    pd.Series(np.random.rand(100), index=np.arange(100)),
    label="Test",
    xlabel="X",
    ylabel="Y",
)
save_figure(fig, "examples/example.html")
