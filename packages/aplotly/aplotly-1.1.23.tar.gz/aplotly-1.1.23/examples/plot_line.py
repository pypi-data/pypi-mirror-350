import numpy as np
import pandas as pd

from aplotly.plots import plot_line

filter_series = pd.Series(np.repeat(np.random.rand(10), 10))
exposure = pd.DataFrame(
    np.random.rand(100, 10), columns=["".join(np.random.choice(["A", "B", "C"], 3)) for _ in range(10)]
)

# fill half of the values with zeros, randomly
random_mask = np.random.choice([True, False], size=exposure.shape)
holdings = exposure.mask(random_mask, 0)

fig = plot_line(
    pd.Series(np.random.rand(100), index=np.arange(100)),
    label="Test",
    xlabel="X",
    ylabel="Y",
    color_palette="dark_mode",
    filter_series=filter_series,
    holdings=holdings,
)
fig.show()
