import numpy as np
import pandas as pd

from aplotly.plots import plot_bars

exposures = pd.DataFrame(
    np.concatenate([np.ones((10, 3)), np.ones((10, 3)) * 0.5]), columns=["a", "b", "c"], index=np.arange(20)
)
exposures = exposures.div(exposures.sum(axis=1), axis=0)

returns = pd.DataFrame(
    np.concatenate([np.ones((20, 1)) * 0.01, np.ones((20, 1)) * 0.02, np.ones((20, 1)) * 0.03], axis=1),
    columns=["a", "b", "c"],
    index=np.arange(20),
)

performance_by_asset = (returns.mul(exposures) + 1).cumprod(axis=0) - 1
asset_performance = (returns + 1).cumprod(axis=0) - 1

performance_by_asset = performance_by_asset.iloc[::5]
asset_performance = asset_performance.iloc[::5]


performance_by_asset.columns = [x + "_pf" for x in performance_by_asset.columns]

performance_by_asset = performance_by_asset.stack().reset_index().set_index("level_0")
asset_performance = asset_performance.stack().reset_index().set_index("level_0")

performance_by_asset.columns = ["asset", "performance"]
asset_performance.columns = ["asset", "performance"]

df = pd.concat([performance_by_asset, asset_performance], axis=0)
df = df.sort_values(["level_0", "asset"])

fig = plot_bars(
    df,
    height_column="performance",
    label_column="asset",
    xlabel="X",
)
fig.show()
