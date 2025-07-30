from unittest import TestCase, main

import plotly.io as pio

from aplotly.colors import select_palette
from aplotly.style import configure_plotly


class TestStyle(TestCase):
    def test_configure(self):
        for subplots in [1, 2, 3]:
            for color_palette in ["default", "greys", "night", "dark_mode"]:
                configure_plotly(subplots, color_palette)
                line_colors, chart_colors = select_palette(color_palette, "rgba")

                # check that "style" in in pio.templates
                self.assertIn("style", pio.templates)

                color_way = []
                for color in list(line_colors.values()):
                    color_way += [color] * subplots
                # check colorway is correct
                self.assertEqual([*pio.templates["style"]["layout"]["colorway"]], color_way)

                # check the background color is correct
                self.assertEqual(pio.templates["style"]["layout"]["paper_bgcolor"], chart_colors["background"])

                # check the grid color is correct
                self.assertEqual(pio.templates["style"]["layout"]["xaxis"]["gridcolor"], chart_colors["grid"])

                # check the text color is correct
                self.assertEqual(pio.templates["style"]["layout"]["title"]["font"]["color"], chart_colors["text"])

                # check the axes color is correct
                self.assertEqual(pio.templates["style"]["layout"]["xaxis"]["linecolor"], chart_colors["axes"])

                # check the legend text color is correct
                self.assertEqual(pio.templates["style"]["layout"]["legend"]["font"]["color"], chart_colors["text"])

                # check the legend title color is correct
                self.assertEqual(
                    pio.templates["style"]["layout"]["legend"]["title_font"]["color"], chart_colors["text"]
                )


if __name__ == "__main__":
    main()
