import pandas as pd

from aplotly.plots import plot_correlation

correlations = pd.DataFrame(
    {
        "a": [1.0, 0.2, 0.2, 0.4, 0.5],
        "b": [0.6, 1.0, 0.8, 0.9, 1.0],
        "c": [0.1, 0.2, 1.0, 0.4, 0.5],
        "d": [0.6, 0.7, 0.8, 1.0, 1.0],
        "e": [0.6, 0.7, 0.8, 1.0, 1.0],
    },
    index=["a", "b", "c", "d", "e"],
)

fig = plot_correlation(
    correlations,
    plot_title="Correlation",
    color_palette="dark_mode",
)

fig.show()
