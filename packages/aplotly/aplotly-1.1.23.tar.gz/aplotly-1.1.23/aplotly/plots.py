from typing import List, Union

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from aplotly.utils.return_breakdown import calculate_return_breakdown

from .style import configure_plotly


def plot_line(
    series: pd.Series,
    label: str,
    xlabel: str,
    ylabel: str,
    legend: bool = True,
    filter_series: Union[pd.Series, None] = None,
    holdings: Union[pd.DataFrame, None] = None,
    color_palette: str = "",
    group_title: str = "",
    plot_title: str = "",
) -> go.Figure:
    """Plot a line chart.

    Args:
        series (pd.Series): data for the line chart, the index is the x-axis and the values are the y-axis.
        label (str): name for the line.
        xlabel (str): x-axis label.
        ylabel (str): y-axis label.
        legend (bool, optional): if the legend should be shown. Defaults to True.
        filter_series (Union[pd.Series, None], optional): filter to show on the plot. Defaults to None (no filter).
        holdings (Union[pd.DataFrame, None], optional): holdings to show on the plot. Defaults to None (no holdings).
        color_palette (str, optional): which color palette to use. Defaults to "" (default color palette).
        group_title (str, optional): name of the group on the legend. Defaults to "" (no group name).
        plot_title (str, optional): title of the plot. Defaults to "" (no title).

    Returns:
        go.Figure: plotly figure containing the line chart.
    """
    if holdings is not None:
        custom_labels = []
        for idx, row in holdings.iterrows():
            if idx not in series.index:
                continue

            custom_string = row[row != 0.0].sort_values(ascending=False).round(3).to_string()
            custom_string = (
                custom_string.replace("    ", ": ")
                .replace("\n", "<br>")
                .replace("  ", " ")
                .replace("Series([], )", "")
            )
            custom_string = "Holdings: <br>" + custom_string
            custom_labels.append(custom_string)
    else:
        custom_labels = None

    configure_plotly(subplots=1, color_palette=color_palette)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=series.index,
            y=series.values,
            mode="lines",
            name=label,
            legendgroup=1,
            legendgrouptitle_text=group_title,
            line=dict(width=2),
            text=custom_labels,
        )
    )

    fig.update_xaxes(title_text=xlabel)
    fig.update_yaxes(title_text=ylabel)
    fig.update_layout(showlegend=legend, title_text=plot_title)

    if filter_series is not None:
        filter_change = filter_series.diff()

        for x, y in zip(series[filter_change > 0].index, series[filter_change > 0].values):
            fig.add_annotation(
                xref="x",
                yref="y",
                x=x,
                y=y,
                xanchor="center",
                yanchor="bottom",
                text="\u2191",
                showarrow=False,
                font=dict(color="cyan" if color_palette in ["dark_mode", "night"] else "green", size=20),
            )

        for x, y in zip(series[filter_change < 0].index, series[filter_change < 0].values):
            fig.add_annotation(
                xref="x",
                yref="y",
                x=x,
                y=y,
                xanchor="center",
                yanchor="bottom",
                text="\u2193",
                showarrow=False,
                font=dict(color="red", size=20),
            )

    return fig


def plot_multiple_lines(
    series: List[pd.Series],
    ylabel: str,
    xlabel: str,
    labels: list = None,
    visible: list = None,
    styles: list = None,
    colors: list = None,
    legend: bool = True,
    color_palette: str = "",
    group_title: str = "",
    plot_title: str = "",
) -> go.Figure:
    """Plot multiple line charts.

    Args:
        series (List[pd.Series]): list of data for the line charts, the index is the x-axis and the values are the y-axis.
        ylabel (str): y-axis label.
        xlabel (str): x-axis label.
        labels (list, optional): name of each line. Defaults to None (doesn't label of the lines).
        visible (list, optional): if the lines should be visible by default. Defaults to None (all lines are visible).
        styles (list, optional): list of line style dictionaries. Defaults to None.
        colors (list, optional): list of colors for each line. Defaults to None (uses default color palette).
        legend (bool, optional): if the legend should be shown. Defaults to True.
        color_palette (str, optional): name of the color palette to use. Defaults to "" (default color palette).
        group_title (str, optional): name of the legend group. Defaults to "" (no group name).
        plot_title (str, optional): title for the plot. Defaults to "" (no title).

    Returns:
        go.Figure: plotly figure containing the line charts.
    """
    if labels is None:
        labels = [None] * len(series)

    if visible is None:
        visible = [True] * len(series)

    if styles is None:
        styles = [{"width": 2}] * len(series)

    if colors is None:
        colors = [None] * len(series)

    if any(visible) is False:
        legend = True

    configure_plotly(subplots=1, color_palette=color_palette)
    fig = go.Figure()
    for data, label, visibility, style, color in zip(series, labels, visible, styles, colors):
        if color is not None:
            style = style.copy() if style is not None else {}
            style["color"] = color
            
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data.values,
                mode="lines",
                name=label,
                legendgroup=1,
                legendgrouptitle_text=group_title,
                visible=visibility,
                line=style,
            )
        )
    fig.update_xaxes(title_text=xlabel)
    fig.update_yaxes(title_text=ylabel)
    fig.update_layout(showlegend=legend, title_text=plot_title)

    return fig


def plot_multiple_lines_with_distribution(
    series: List[pd.Series],
    ylabel: str,
    xlabel: str,
    labels: list = None,
    visible: list = None,
    styles: list = None,
    legend: bool = True,
    color_palette: str = "",
    group_title: str = "",
    plot_title: str = "",
    hist_width: float = 0.2,
    n_bins: int = 10,
) -> go.Figure:
    """Plot multiple line charts with a distribution histogram of final values.

    Args:
        series (List[pd.Series]): list of data for the line charts, the index is the x-axis and the values are the y-axis.
        ylabel (str): y-axis label.
        xlabel (str): x-axis label.
        labels (list, optional): name of each line. Defaults to None (doesn't label of the lines).
        visible (list, optional): if the lines should be visible by default. Defaults to None (all lines are visible).
        styles (list, optional): list of line style dictionaries. Defaults to None.
        legend (bool, optional): if the legend should be shown. Defaults to True.
        color_palette (str, optional): name of the color palette to use. Defaults to "" (default color palette).
        group_title (str, optional): name of the legend group. Defaults to "" (no group name).
        plot_title (str, optional): title for the plot. Defaults to "" (no title).
        hist_width (float, optional): relative width of histogram panel. Defaults to 0.2.
        n_bins (int, optional): number of bins for the histogram. Defaults to 10.

    Returns:
        go.Figure: plotly figure containing the line charts and distribution histogram.
    """
    if labels is None:
        labels = [None] * len(series)

    if visible is None:
        visible = [True] * len(series)

    if styles is None:
        styles = [{"width": 2}] * len(series)

    if any(visible) is False:
        legend = True

    configure_plotly(subplots=1, color_palette=color_palette)

    # Create subplot with shared y-axis
    fig = make_subplots(
        rows=1, cols=2, column_widths=[1 - hist_width, hist_width], shared_yaxes=True, horizontal_spacing=0.02
    )

    # Add line traces
    final_values = []
    for data, label, visibility, style in zip(series, labels, visible, styles):
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data.values,
                mode="lines",
                name=label,
                legendgroup=1,
                legendgrouptitle_text=group_title,
                visible=visibility,
                line=style,
            ),
            row=1,
            col=1,
        )
        if visibility:
            final_values.append(data.iloc[-1])

    # Calculate statistics
    mean_val = sum(final_values) / len(final_values)
    std_val = (sum((x - mean_val) ** 2 for x in final_values) / len(final_values)) ** 0.5

    # Add single histogram trace for all final values
    hist_trace = go.Histogram(
        y=final_values,
        name="Distribution",
        legendgroup=1,
        showlegend=False,
        orientation="h",
        nbinsy=n_bins,
        marker_color="rgb(192, 192, 192)",  # Light grey color
    )
    fig.add_trace(hist_trace, row=1, col=2)

    # Calculate max count using numpy's histogram
    import numpy as np

    counts, _ = np.histogram(final_values, bins=n_bins)
    max_count = max(counts)

    # Add mean line with extended range
    fig.add_trace(
        go.Scatter(
            x=[-0.1 * max_count, 1.1 * max_count],
            y=[mean_val, mean_val],
            mode="lines",
            line=dict(color="black", width=2),
            name="Mean",
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    # Add std lines with extended range
    for std_level in [mean_val - std_val, mean_val + std_val]:
        fig.add_trace(
            go.Scatter(
                x=[-0.1 * max_count, 1.1 * max_count],
                y=[std_level, std_level],
                mode="lines",
                line=dict(color="black", width=1, dash="dash"),
                name="±1 std",
                showlegend=False,
            ),
            row=1,
            col=2,
        )

    # Update layout
    fig.update_xaxes(title_text=xlabel, row=1, col=1)
    fig.update_yaxes(title_text=ylabel, row=1, col=1)
    fig.update_xaxes(title_text="Count", row=1, col=2)
    fig.update_layout(
        showlegend=legend,
        title_text=plot_title,
        bargap=0,  # Remove gaps between bars
        bargroupgap=0,  # Remove gaps between groups
    )

    # Set x-axis range for histogram panel
    fig.update_xaxes(range=[0, max_count], row=1, col=2)

    return fig


def plot_performance(
    performance: pd.Series,
    drawdown: pd.Series,
    performance_label: str,
    drawdown_label: str,
    performance_ylabel: str = "PnL (%)",
    drawdown_ylabel: str = "Drawdown (%)",
    xlabel: str = "Date",
    legend: bool = True,
    color_palette: str = "",
    performance_group_title: str = "Performance",
    drawdown_group_title: str = "Drawdown",
    row_heights: list = [0.7, 0.3],
    vertical_spacing: float = 0.02,
    plot_title: str = "",
) -> go.Figure:
    """Plot the performance and drawdown of a strategy.

    Returns a double panel plot with the performance on the top and the drawdown on the bottom.

    Args:
        performance (pd.Series): data for the performance, the index is the x-axis and the values are the y-axis.
        drawdown (pd.Series): data for the drawdown, the index is the x-axis and the values are the y-axis.
        performance_label (str): name for the performance line.
        drawdown_label (str): name for the drawdown line.
        performance_ylabel (str, optional): performance y-axis label. Defaults to "PnL (%)".
        drawdown_ylabel (str, optional): drawdown y-axis label. Defaults to "Drawdown (%)".
        xlabel (str, optional): x-axis label. Defaults to "Date".
        legend (bool, optional): if the legend should be shown. Defaults to True.
        color_palette (str, optional): name of the color palette to use. Defaults to "" (default color palette).
        performance_group_title (str, optional): name for the performance legend group. Defaults to "Performance".
        drawdown_group_title (str, optional): name for the drawdown legend group. Defaults to "Drawdown".
        row_heights (list, optional): height of each row. Defaults to [0.7, 0.3].
        vertical_spacing (float, optional): vertical spacing between rows. Defaults to 0.02.
        plot_title (str, optional): title for the plot. Defaults to "" (no title).

    Returns:
        go.Figure: plotly figure containing the performance and drawdown.
    """
    configure_plotly(subplots=2, color_palette=color_palette)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=vertical_spacing, row_heights=row_heights)
    fig.add_trace(
        go.Scatter(
            x=performance.index,
            y=performance,
            mode="lines",
            name=performance_label,
            legendgroup=1,
            legendgrouptitle_text=performance_group_title,
            line=dict(width=2),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=drawdown.index,
            y=drawdown,
            mode="lines",
            name=drawdown_label,
            legendgroup=2,
            legendgrouptitle_text=drawdown_group_title,
            line=dict(width=2),
        ),
        row=2,
        col=1,
    )

    fig.update_yaxes(title_text=performance_ylabel, row=1, col=1)
    fig.update_yaxes(title_text=drawdown_ylabel, row=2, col=1)
    fig.update_xaxes(title_text=xlabel, row=2, col=1)
    fig.update_layout(showlegend=legend, title_text=plot_title)

    return fig


def plot_multiple_performance(
    performance: List[pd.Series],
    drawdown: List[pd.Series],
    labels: list = None,
    performance_ylabel: str = "PnL (%)",
    drawdown_ylabel: str = "Drawdown (%)",
    xlabel: str = "Date",
    legend: bool = True,
    color_palette: str = "",
    performance_group_title: str = "Performance",
    drawdown_group_title: str = "Drawdown",
    row_heights: list = [0.7, 0.3],
    vertical_spacing: float = 0.02,
    plot_title: str = "",
) -> go.Figure:
    """Plot the performance and drawdown of multiple strategies.

    Returns a double panel plot with the performance on the top and the drawdown on the bottom.

    Args:
        performance (List[pd.Series]): list of data for the performance, the index is the x-axis and the values are the y-axis.
        drawdown (List[pd.Series]): list of data for the drawdown, the index is the x-axis and the values are the y-axis.
        labels (list, optional): name for each strategy. Defaults to None (no labels).
        performance_ylabel (str, optional): performance y-axis label. Defaults to "PnL (%)".
        drawdown_ylabel (str, optional): drawdown y-axis label. Defaults to "Drawdown (%)".
        xlabel (str, optional): x-axis label. Defaults to "Date".
        legend (bool, optional): if the legend should be shown. Defaults to True.
        color_palette (str, optional): name of the color palette to use. Defaults to "" (default color palette).
        performance_group_title (str, optional): name for the performance legend group. Defaults to "Performance".
        drawdown_group_title (str, optional): name for the drawdown legend group. Defaults to "Drawdown".
        row_heights (list, optional): height of each row. Defaults to [0.7, 0.3].
        vertical_spacing (float, optional): vertical spacing between rows. Defaults to 0.02.
        plot_title (str, optional): title for the plot. Defaults to "" (no title).

    Returns:
        go.Figure: plotly figure containing the performance and drawdown.

    """
    if len(performance) != len(drawdown):
        raise ValueError("performance and drawdown must have the same length")

    if labels is None:
        labels = [None] * len(performance)

    configure_plotly(subplots=2, color_palette=color_palette)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=vertical_spacing, row_heights=row_heights)
    for _performance, _drawdown, label in zip(performance, drawdown, labels):
        fig.add_trace(
            go.Scatter(
                x=_performance.index,
                y=_performance,
                mode="lines",
                name=label,
                legendgroup=1,
                legendgrouptitle_text=performance_group_title,
                line=dict(width=2),
            ),
            row=1,
            col=1,
        )

        fig.for_each_trace(lambda trace: trace.update(line=dict(color=trace.marker.color)))

        fig.add_trace(
            go.Scatter(
                x=_drawdown.index,
                y=_drawdown,
                mode="lines",
                name=label,
                legendgroup=2,
                legendgrouptitle_text=drawdown_group_title,
                line=dict(width=2),
            ),
            row=2,
            col=1,
        )

    fig.update_yaxes(title_text=performance_ylabel, row=1, col=1)
    fig.update_yaxes(title_text=drawdown_ylabel, row=2, col=1)
    fig.update_xaxes(title_text=xlabel, row=2, col=1)
    fig.update_layout(showlegend=legend, title_text=plot_title)

    return fig


def plot_bars(
    df: pd.DataFrame,
    height_column: str,
    label_column: str = None,
    ylabel: str = "",
    xlabel: str = "",
    legend: bool = True,
    color_palette: str = "",
    group_title: str = "",
    plot_title: str = "",
) -> go.Figure:
    """Plot a bar chart.

    Args:
        df (pd.DataFrame): data for the bar chart, the index is the x-axis and the columns should contain the bar heights and (optionally) the labels.
        height_column (str): name of the column containing the height of the bars.
        label_column (str, optional): name of the column containing the labels for the bars. Defaults to None (no labels).
        ylabel (str, optional): y-axis label. Defaults to "" (no label).
        xlabel (str, optional): x-axis label. Defaults to "" (no label).
        legend (bool, optional): if the legend should be shown. Defaults to True.
        color_palette (str, optional): name of the color palette to use. Defaults to "" (default color palette).
        group_title (str, optional): name of the legend group. Defaults to "" (no group name).
        plot_title (str, optional): title for the plot. Defaults to "" (no title).

    Returns:
        go.Figure: plotly figure containing the bar chart.
    """
    configure_plotly(subplots=1, color_palette=color_palette)

    if label_column is not None:
        labels = df[label_column].unique()
        heights = {label: df[df[label_column] == label][height_column] for label in labels}
        indicies = {label: df[df[label_column] == label].index for label in labels}

        data = [
            go.Bar(name=label, x=indicies[label], y=heights[label], legendgroup=1, legendgrouptitle_text=group_title)
            for label in labels
        ]

    else:
        data = [go.Bar(x=df.index, y=df[height_column], legendgroup=1, legendgrouptitle_text=group_title)]

    fig = go.Figure(data=data)

    fig.update_yaxes(title_text=ylabel)
    fig.update_xaxes(title_text=xlabel)
    fig.update_layout(showlegend=legend, title_text=plot_title, barmode="group")

    return fig


def plot_returns_tree(
    returns: pd.DataFrame,
    exposure: pd.DataFrame,
    metric: str = "total_return",
    root_color: str = "black",
    color_path: list = ["red", "grey", "green"],
    color_bar: bool = False,
    plot_title: str = "",
):
    """Plot a tree map of the returns.

    Args:
        returns (pd.DataFrame): return data, the index is the date and the columns are the instruments.
        exposure (pd.DataFrame): exposure data, the index is the date and the columns are the instruments.
        metric (str, optional): metric to use for the tree map. Defaults to "total_return",
            choices are "max_return", "avg_return", "std_return" or "total_return".
        root_color (str, optional): color of the root node. Defaults to "black".
        color_path (list, optional): color path for the tree map. Defaults to ["red", "grey", "green"].
            This is used to create a color gradient from the worst performing instrument to the best performing (first color) to the best performing (last color).
        color_bar (bool, optional): if the color bar should be shown. Defaults to False.
        plot_title (str, optional): title for the plot. Defaults to "" (no title).

    Returns:
        go.Figure: plotly figure containing the tree map.

    Raises:
        ValueError: if metric is not one of "max_return", "avg_return", "std_return" or "total_return".

    """
    if metric not in ["max_return", "avg_return", "std_return", "total_return"]:
        raise ValueError("metric must be either 'max_return', 'avg_return', 'std_return' or 'total_return'")

    if metric == "total_return":
        return plot_return_breakdown(returns, exposure, root_color, color_path, color_bar, plot_title)

    metrics = []
    for column in exposure.columns:
        _exposure = exposure[column]
        _exposure = _exposure[_exposure != 0]
        try:
            _metrics = {
                "name": column,
                "max_return": returns.loc[_exposure.index, column].max(),
                "avg_return": returns.loc[_exposure.index, column].mean(),
                "std_return": returns.loc[_exposure.index, column].std(),
            }
            metrics.append(_metrics)
        except:
            continue

    sizes = metrics[metric].abs()
    colors = metrics[metric]
    labels = metrics["name"]

    configure_plotly(1, "")
    fig = go.Figure(
        go.Treemap(
            labels=labels,
            parents=[""] * len(labels),
            values=sizes,
            customdata=colors,
            hovertemplate="<b>%{label}</b><br>%{customdata:.2%}<extra></extra>",
            texttemplate="%{label}<br>%{customdata:.2%}",
            textposition="middle center",
            textfont=dict(size=18),
            marker=dict(
                colors=colors,
                colorscale=color_path,
                cmid=0,
                showscale=color_bar,
                line=dict(width=0),
            ),
            tiling=dict(
                packing="squarify",
                pad=1,
            ),
            root_color=root_color,
        )
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), title_text=plot_title)

    fig.data[0].customdata = colors.values
    fig.data[0].texttemplate = "%{label}<br>%{customdata:.2%}"

    return fig


def plot_return_breakdown(
    returns: pd.DataFrame,
    exposure: pd.DataFrame,
    root_color: str = "black",
    color_path: list = ["red", "grey", "green"],
    color_bar: bool = False,
    plot_title: str = "",
    attribution_only: bool = False,
):
    returns = calculate_return_breakdown(exposure, returns)
    relative_returns = returns / returns.sum()

    labels = returns.index
    sizes = returns.abs()
    colors = returns

    configure_plotly(1, "")
    fig = go.Figure(
        go.Treemap(
            labels=labels,
            parents=[""] * len(labels),
            values=sizes,
            customdata=colors,
            hovertemplate="<b>%{label}</b><br>%{customdata:.2%}<extra></extra>",
            texttemplate="%{label}<br>%{customdata:.2%}",
            textposition="middle center",
            textfont=dict(size=18),
            marker=dict(
                colors=colors,
                colorscale=color_path,
                cmid=0,
                showscale=color_bar,
                line=dict(width=0),
            ),
            tiling=dict(
                packing="squarify",
                pad=1,
            ),
            root_color=root_color,
        )
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), title_text=plot_title)

    if attribution_only:
        fig.data[0].customdata = [r for r in relative_returns]
        fig.data[0].texttemplate = "%{label}<br>%{customdata:.2%}"

    else:
        fig.data[0].customdata = [(r, _r) for r, _r in zip(returns, relative_returns)]
        fig.data[0].texttemplate = "%{label}<br>%{customdata[0]:.2%}<br><i>%{customdata[1]:.2%}</i>"

    return fig


def plot_exposure_tree(
    exposure: pd.Series,
    root_color: str = "black",
    color_path: list = ["red", "grey", "green"],
    color_bar: bool = False,
    plot_title: str = "",
):
    """Plot a tree map of the exposure.

    Args:
        exposure (pd.Series): exposure data, the index is the instruments.
        root_color (str, optional): color of the root node. Defaults to "black".
        color_path (list, optional): color path for the tree map. Defaults to ["red", "grey", "green"].
            This is used to create a color gradient from the worst performing instrument to the best performing (first color) to the best performing (last color).
        color_bar (bool, optional): if the color bar should be shown. Defaults to False.
        plot_title (str, optional): title for the plot. Defaults to "" (no title).
    """
    labels = exposure.index
    sizes = exposure.abs()
    colors = exposure

    configure_plotly(1, "")
    fig = go.Figure(
        go.Treemap(
            labels=labels,
            parents=[""] * len(labels),
            values=sizes,
            customdata=colors,
            hovertemplate="<b>%{label}</b><br>%{customdata:.2%}<extra></extra>",
            texttemplate="%{label}<br>%{customdata:.2%}",
            textposition="middle center",
            textfont=dict(size=18),
            marker=dict(
                colors=colors,
                colorscale=color_path,
                cmid=0,
                showscale=color_bar,
                line=dict(width=0),
            ),
            tiling=dict(
                packing="squarify",
                pad=1,
            ),
            root_color=root_color,
        )
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), title_text=plot_title)

    fig.data[0].customdata = colors.values
    fig.data[0].texttemplate = "%{label}<br>%{customdata:.2%}"

    return fig


def plot_gauge(
    value,
    previous_value: Union[float, None] = None,
    threshold: Union[float, None] = None,
    gauge_range=(0, 100),
    color_palette: str = "",
    plot_title: str = "",
):
    """Plot a gauge chart.

    Args:
        value (float): value to show on the gauge.
        previous_value (Union[float, None]): optional previous value to use for delta. Defaults to None.
        threshold (Union[float, None], optional): threshold value. Defaults to None.
        gauge_range (tuple, optional): range of the gauge. Defaults to (0, 100).
        color_palette (str, optional): name of the color palette to use. Defaults to "" (default color palette).
        plot_title (str, optional): title for the plot. Defaults to "" (no title).

    """
    _, chart_colors = configure_plotly(subplots=1, color_palette=color_palette)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta" if previous_value is not None else "gauge+number",
            value=value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": plot_title},
            delta={"reference": previous_value},
            gauge={
                "axis": {"range": gauge_range},
                "threshold": {
                    "line": {"color": chart_colors["text"]},
                    "thickness": 0.75,
                    "value": threshold if threshold is not None else None,
                },
            },
        )
    )

    return fig


def plot_performance_by_trade(
    pbt: pd.DataFrame,
    marker_size: int = 10,
    color_palette: str = "",
    plot_title: str = "",
):
    configure_plotly(subplots=4, color_palette=color_palette)
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    fig.add_trace(
        go.Scatter(
            x=pbt.index,
            y=pbt["hit_rate"] * 100,
            mode="lines+markers",
            name="Portfolio",
            legendgroup=1,
            legendgrouptitle_text="Hit Rate",
            line=dict(width=2),
            marker={"size": marker_size},
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=pbt.index,
            y=pbt["slugging_ratio"],
            mode="lines+markers",
            name="Portfolio",
            legendgroup=2,
            legendgrouptitle_text="Slugging Ratio",
            line=dict(width=2),
            marker={"size": marker_size},
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=pbt.index,
            y=pbt["average_win"] * 100,
            mode="lines+markers",
            name="Portfolio",
            legendgroup=3,
            legendgrouptitle_text="Average Win",
            line=dict(width=2),
            marker={"size": marker_size},
        ),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=pbt.index,
            y=pbt["trades"],
            name="Portfolio",
            legendgroup=4,
            legendgrouptitle_text="Trades",
            marker_line_width=0,
        ),
        row=4,
        col=1,
    )

    # add a straight horizontal line at 50% hit rate
    fig.add_shape(
        type="line",
        x0=pbt.index[0],
        y0=50,
        x1=pbt.index[-1],
        y1=50,
        line=dict(color="grey", width=1, dash="dash"),
        row=1,
        col=1,
    )

    fig.update_yaxes(title_text="Hit Rate (%)", row=1, col=1)
    fig.update_yaxes(title_text="Slugging Ratio", row=2, col=1)
    fig.update_yaxes(title_text="Average Win (%)", row=3, col=1)
    fig.update_yaxes(title_text="Trades", row=4, col=1)
    fig.update_xaxes(title_text="Date", row=4, col=1)
    fig.update_layout(title_text=plot_title)

    return fig


def plot_correlation(
    correlation: pd.DataFrame,
    color_palette: str = "",
    plot_title: str = "",
):
    """Plot a correlation matrix.

    Args:
        correlation (pd.DataFrame): correlation matrix.
        color_palette (str, optional): name of the color palette to use. Defaults to "" (default color palette).
        plot_title (str, optional): title for the plot. Defaults to "" (no title).

    Returns:
        go.Figure: plotly figure containing the correlation matrix.
    """
    configure_plotly(subplots=1, color_palette=color_palette)
    fig = go.Figure(
        go.Heatmap(
            z=correlation,
            x=correlation.columns,
            y=correlation.columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            colorbar=dict(title="Correlation"),
        )
    )

    fig.update_layout(title_text=plot_title, yaxis={"scaleanchor": "x", "scaleratio": 1})

    return fig


def plot_confidence_intervals(
    series: List[pd.Series],
    ylabel: str,
    xlabel: str,
    label: str = "Mean",
    legend: bool = True,
    color_palette: str = "",
    group_title: str = "",
    plot_title: str = "",
    hist_width: float = 0.2,
    n_bins: int = 10,
    poly_degree: int = 0,  # 0 means no polynomial fitting, otherwise specifies polynomial degree
    show_underlying: bool = False,  # whether to show the underlying lines
) -> go.Figure:
    """Plot mean with confidence intervals and distribution of final values.

    Args:
        series (List[pd.Series]): list of data series to combine.
        ylabel (str): y-axis label.
        xlabel (str): x-axis label.
        label (str, optional): name for the mean line. Defaults to "Mean".
        legend (bool, optional): if the legend should be shown. Defaults to True.
        color_palette (str, optional): name of the color palette to use. Defaults to "" (default color palette).
        group_title (str, optional): name of the legend group. Defaults to "" (no group name).
        plot_title (str, optional): title for the plot. Defaults to "" (no title).
        hist_width (float, optional): relative width of histogram panel. Defaults to 0.2.
        n_bins (int, optional): number of bins for the histogram. Defaults to 10.
        poly_degree (int, optional): degree of polynomial fitting. 0 means no polynomial fitting. Defaults to 0.
        show_underlying (bool, optional): whether to show the underlying lines. Defaults to False.

    Returns:
        go.Figure: plotly figure containing the mean, confidence intervals, and distribution.
    """
    # Combine series into a DataFrame
    df = pd.concat(series, axis=1)

    # Calculate mean and std at each point
    mean = df.mean(axis=1)
    std = df.std(axis=1)

    # Apply polynomial fitting if requested
    if poly_degree > 0:
        import numpy as np

        x = np.arange(len(mean))

        # Create coefficient matrices without constant term (to enforce zero intercept)
        # For mean
        X_mean = np.vstack([x ** (i + 1) for i in range(poly_degree)]).T
        mean_coeffs = np.linalg.lstsq(X_mean, mean, rcond=None)[0]
        mean = pd.Series(np.dot(X_mean, mean_coeffs), index=mean.index)

        # For std
        X_std = np.vstack([x ** (i + 1) for i in range(poly_degree)]).T
        std_coeffs = np.linalg.lstsq(X_std, std, rcond=None)[0]
        std = pd.Series(np.dot(X_std, std_coeffs), index=std.index)

    # Calculate confidence intervals
    ci_95 = 1.96 * std  # 95% confidence interval
    ci_99 = 2.576 * std  # 99% confidence interval

    configure_plotly(subplots=1, color_palette=color_palette)

    # Create subplot with shared y-axis
    fig = make_subplots(
        rows=1, cols=2, column_widths=[1 - hist_width, hist_width], shared_yaxes=True, horizontal_spacing=0.02
    )

    # Add underlying lines if requested
    if show_underlying:
        for i, s in enumerate(series):
            fig.add_trace(
                go.Scatter(
                    x=s.index,
                    y=s.values,
                    mode="lines",
                    name=f"Series {i+1}",
                    legendgroup=2,
                    legendgrouptitle_text="Individual Series",
                    line=dict(width=1, color="rgba(128, 128, 128, 0.3)"),
                    showlegend=False,
                ),
                row=1,
                col=1,
            )

    # Add mean line
    fig.add_trace(
        go.Scatter(
            x=mean.index,
            y=mean,
            mode="lines",
            name=label,
            legendgroup=1,
            legendgrouptitle_text=group_title,
            line=dict(width=2, color="black"),
        ),
        row=1,
        col=1,
    )

    # Add 95% confidence interval
    fig.add_trace(
        go.Scatter(
            x=mean.index,
            y=mean + ci_95,
            mode="lines",
            name="95% CI",
            line=dict(width=0),
            legendgroup=1,
            showlegend=True,
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=mean.index,
            y=mean - ci_95,
            mode="lines",
            name="95% CI",
            fill="tonexty",
            fillcolor="rgba(68, 68, 68, 0.2)",
            line=dict(width=0),
            legendgroup=1,
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    # Add 99% confidence interval
    fig.add_trace(
        go.Scatter(
            x=mean.index,
            y=mean + ci_99,
            mode="lines",
            name="99% CI",
            line=dict(width=0),
            legendgroup=1,
            showlegend=True,
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=mean.index,
            y=mean - ci_99,
            mode="lines",
            name="99% CI",
            fill="tonexty",
            fillcolor="rgba(68, 68, 68, 0.1)",
            line=dict(width=0),
            legendgroup=1,
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    # Add histogram of final values
    final_values = df.iloc[-1]
    hist_trace = go.Histogram(
        y=final_values,
        name="Distribution",
        legendgroup=1,
        showlegend=False,
        orientation="h",
        nbinsy=n_bins,
        marker_color="rgb(192, 192, 192)",
    )
    fig.add_trace(hist_trace, row=1, col=2)

    # Calculate max count for histogram scaling
    import numpy as np

    counts, _ = np.histogram(final_values, bins=n_bins)
    max_count = max(counts)

    # Add mean line to histogram
    final_mean = final_values.mean()
    final_std = final_values.std()
    fig.add_trace(
        go.Scatter(
            x=[-0.1 * max_count, 1.1 * max_count],
            y=[final_mean, final_mean],
            mode="lines",
            line=dict(color="black", width=2),
            name="Mean",
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    # Add std lines to histogram
    for std_level in [final_mean - final_std, final_mean + final_std]:
        fig.add_trace(
            go.Scatter(
                x=[-0.1 * max_count, 1.1 * max_count],
                y=[std_level, std_level],
                mode="lines",
                line=dict(color="black", width=1, dash="dash"),
                name="±1 std",
                showlegend=False,
            ),
            row=1,
            col=2,
        )

    # Update layout
    fig.update_xaxes(title_text=xlabel, row=1, col=1)
    fig.update_yaxes(title_text=ylabel, row=1, col=1)
    fig.update_xaxes(title_text="Count", row=1, col=2)
    fig.update_xaxes(range=[0, max_count], row=1, col=2)
    fig.update_layout(
        showlegend=legend,
        title_text=plot_title,
        bargap=0,
        bargroupgap=0,
    )

    return fig


def plot_benchmark_portfolio_returns(
    benchmark_returns: pd.Series,
    portfolio_returns: pd.Series,
    positive_months: bool = True,
    color_palette: str = "",
    plot_title: str = None,
    benchmark_name: str = "Benchmark",
    portfolio_name: str = "Portfolio",
) -> go.Figure:
    """Plot a double bar chart showing benchmark returns and portfolio returns for either positive or negative months.
    
    Args:
        benchmark_returns (pd.Series): Series containing benchmark returns data.
        portfolio_returns (pd.Series): Series containing portfolio returns data.
        positive_months (bool, optional): If True, show positive months; if False, show negative months. Defaults to True.
        color_palette (str, optional): Color palette to use. Defaults to "".
        plot_title (str, optional): Title for the plot. Defaults to None (no title).
        benchmark_name (str, optional): Name of the benchmark for display. Defaults to "Benchmark".
        portfolio_name (str, optional): Name of the portfolio for display. Defaults to "Portfolio".
        
    Returns:
        go.Figure: Plotly figure containing the double bar chart.
    """
    # Configure plotly style
    configure_plotly(subplots=2, color_palette=color_palette)
    
    # Create subplot with shared x-axis and small gap
    fig = make_subplots(
        rows=2, 
        cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.05,  # Add small gap between plots
        row_heights=[0.5, 0.5],
        subplot_titles=("", "")  # Remove subplot titles from top
    )
    
    # Filter for positive or negative months based on benchmark returns
    if positive_months:
        filtered_months = benchmark_returns[benchmark_returns > 0].index
        title_suffix = "Positive"
    else:
        filtered_months = benchmark_returns[benchmark_returns < 0].index
        title_suffix = "Negative"
    
    # Get the filtered data
    filtered_benchmark = benchmark_returns.loc[filtered_months]
    filtered_portfolio = portfolio_returns.loc[filtered_months]
    
    # Define colors
    benchmark_color = "orange"
    portfolio_color = "blue"
    portfolio_negative_color = "darkblue"  # Darker blue for negative portfolio returns
    
    # Add benchmark returns bar chart
    fig.add_trace(
        go.Bar(
            x=filtered_benchmark.index,
            y=filtered_benchmark * 100,  # Convert to percentage
            name=f"{benchmark_name} Returns",
            marker_color=benchmark_color,
        ),
        row=1, col=1
    )
    
    # Split portfolio returns into positive and negative for different colors
    positive_portfolio = filtered_portfolio[filtered_portfolio > 0]
    negative_portfolio = filtered_portfolio[filtered_portfolio < 0]
    
    # Add positive portfolio returns bar chart
    if not positive_portfolio.empty:
        fig.add_trace(
            go.Bar(
                x=positive_portfolio.index,
                y=positive_portfolio * 100,  # Convert to percentage
                name=f"{portfolio_name} Positive Returns",
                marker_color=portfolio_color,
            ),
            row=2, col=1
        )
    
    # Add negative portfolio returns bar chart with darker color
    if not negative_portfolio.empty:
        fig.add_trace(
            go.Bar(
                x=negative_portfolio.index,
                y=negative_portfolio * 100,  # Convert to percentage
                name=f"{portfolio_name} Negative Returns",
                marker_color=portfolio_negative_color,
            ),
            row=2, col=1
        )
    
    # Update layout
    if plot_title is not None:
        title_text = f"{plot_title} ({title_suffix} {benchmark_name} Months)"
    else:
        title_text = None
        
    fig.update_layout(
        title_text=title_text,
        showlegend=False,
        height=800,
        margin=dict(l=50, r=50, t=50, b=50),  # Standard margins
    )
    
    # Update x-axis label
    fig.update_xaxes(title_text="Month", row=2, col=1)
    
    # Add y-axis labels with custom colors
    fig.update_yaxes(
        title_text=f"{benchmark_name} Return (%)", 
        row=1, 
        col=1,
        title_font=dict(color=benchmark_color),
        title_standoff=15
    )
    
    fig.update_yaxes(
        title_text=f"{portfolio_name} Return (%)", 
        row=2, 
        col=1,
        title_font=dict(color=portfolio_color),
        title_standoff=15
    )
    
    return fig
