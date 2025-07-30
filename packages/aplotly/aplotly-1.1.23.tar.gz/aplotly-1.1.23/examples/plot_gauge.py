from aplotly.plots import plot_gauge

value = 100

fig = plot_gauge(
    value=value,
    previous_value=40,
    threshold=50,
    gauge_range=(-100, 200),
    plot_title="Gauge",
    color_palette="dark_mode",
)
fig.show()
