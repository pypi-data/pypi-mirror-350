import numpy as np
import pandas as pd

from aplotly.plots import plot_bars

df = pd.DataFrame({"height": np.random.uniform(0, 1, 10), "label": ["a", "b"] * 5}, index=np.arange(5).tolist() * 2)

fig = plot_bars(
    df,
    height_column="height",
    label_column="label",
    xlabel="X",
)
fig.show()
