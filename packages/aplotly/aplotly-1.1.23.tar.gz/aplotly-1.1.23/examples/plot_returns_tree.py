import numpy as np
import pandas as pd

from aplotly.plots import plot_returns_tree

exposures = pd.DataFrame(
    np.concatenate([np.ones((10, 3)), np.ones((10, 3)) * 0.5]), columns=["a", "b", "c"], index=np.arange(20)
)
exposures = exposures.div(exposures.sum(axis=1), axis=0)

returns = pd.DataFrame(
    np.concatenate([np.ones((20, 1)) * 0.01, np.ones((20, 1)) * 0.02, np.ones((20, 1)) * 0.03], axis=1),
    columns=["a", "b", "c"],
    index=np.arange(20),
)

fig = plot_returns_tree(
    returns,
    exposures,
    metric="total_return",
    root_color="black",
    color_path=["red", "grey", "green"],
    color_bar=False,
    plot_title="Returns Tree",
)
fig.show()
