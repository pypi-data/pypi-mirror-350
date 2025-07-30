from unittest import TestCase, main
from unittest.mock import patch

import plotly.graph_objects as go

from aplotly.io import save_figure, save_html, save_png, save_svg


class TestIO(TestCase):
    def test_save_figure(self):
        with patch("src.io.save_html") as mock_save_html:
            save_figure(None, "test.html")
            mock_save_html.assert_called_once()

        with patch("src.io.save_png") as mock_save_png:
            save_figure(None, "test.png")
            mock_save_png.assert_called_once()

        with patch("src.io.save_svg") as mock_save_svg:
            save_figure(None, "test.svg")
            mock_save_svg.assert_called_once()

        with self.assertRaises(ValueError):
            save_figure(None, "path_without_extension")

        with self.assertRaises(ValueError):
            save_figure(None, "test.fakeext")

        with self.assertRaises(ValueError):
            save_figure(None, "test.pngfakeext")

        with self.assertRaises(ValueError):
            save_figure(None, "test.fakepng")

    def test_save_html(self):
        # create a patch writing to a file
        with patch("builtins.open", create=True) as mock_open:
            fig = go.Figure()

            # call save_html
            save_html(fig, "dev/null")

            # assert that open was called once
            mock_open.assert_called_once()

    def test_save_png(self):
        # create a patch writing to a file
        with patch("plotly.graph_objects.Figure.write_image") as mock_write_image:
            fig = go.Figure()

            # call save_png
            save_png(fig, "dev/null")

            # assert that go.Figure.write_image was called once
            mock_write_image.assert_called_once()

    def test_save_svg(self):
        # create a patch writing to a file
        with patch("plotly.graph_objects.Figure.write_image") as mock_write_image:
            fig = go.Figure()

            # call save_svg
            save_svg(fig, "dev/null")

            # assert that go.Figure.write_image was called once
            mock_write_image.assert_called_once()


if __name__ == "__main__":
    main()
