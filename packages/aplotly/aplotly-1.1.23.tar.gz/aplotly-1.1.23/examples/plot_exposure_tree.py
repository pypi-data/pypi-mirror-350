import numpy as np
import pandas as pd

from aplotly.plots import plot_exposure_tree

exposures = pd.DataFrame(np.random.uniform(-1, 1, (10, 3)), columns=["a", "b", "c"], index=np.arange(10))
exposures = pd.Series([0.1, 0.2, 0.3, -0.1, -0.2, -0.3], index=["a", "b", "c", "d", "e", "f"])

fig = plot_exposure_tree(
    exposures, root_color="black", color_path=["blue", "grey", "green"], color_bar=False, plot_title="Returns Tree"
)
fig.show()
