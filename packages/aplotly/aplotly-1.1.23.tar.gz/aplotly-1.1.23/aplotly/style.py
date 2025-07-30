import os

import plotly.graph_objects as go
import plotly.io as pio

from .colors import select_palette


def configure_plotly(subplots=1, color_palette=""):
    """Configure plotly

    Args:
        subplots (int, optional): number of subplots. Defaults to 1.
        color_palette (str, optional): name of the color palette. Defaults to "" (default palette).

    Returns:
        dict, dict: line_colors, chart_colors
    """
    if os.environ.get("COLOR_PALETTE") is not None:
        color_palette = os.environ.get("COLOR_PALETTE")

    line_colors, chart_colors = select_palette(color_palette, "rgba")

    # duplicate the colors for each subplot
    colorway = []
    for color in list(line_colors.values()):
        colorway += [color] * subplots

    pio.templates["style"] = go.layout.Template(
        layout=go.Layout(
            title=dict(font=dict(size=20, color=chart_colors["text"])),
            colorway=colorway,
            font=dict(size=15, color=chart_colors["text"]),
            paper_bgcolor=chart_colors["background"],
            plot_bgcolor=chart_colors["background"],
            margin=dict(l=80, r=10, t=50, b=80),
            hovermode="closest",
            legend=dict(
                font=dict(size=10, color=chart_colors["text"]),
                title_font=dict(size=15, color=chart_colors["text"]),
                groupclick="toggleitem",
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor=chart_colors["grid"],
                gridwidth=1,
                zeroline=False,
                showline=True,
                linecolor=chart_colors["axes"],
                linewidth=1,
                mirror=True,
                ticks="outside",
                tickcolor=chart_colors["axes"],
                tickwidth=1,
                ticklen=5,
                tickfont=dict(size=10, color=chart_colors["text"]),
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=chart_colors["grid"],
                gridwidth=1,
                zeroline=False,
                showline=True,
                linecolor=chart_colors["axes"],
                linewidth=1,
                mirror=True,
                ticks="outside",
                tickcolor=chart_colors["axes"],
                tickwidth=1,
                ticklen=5,
                tickfont=dict(size=10, color=chart_colors["text"]),
            ),
        )
    )
    pio.templates.default = "style"

    return line_colors, chart_colors
