from unittest import TestCase, main

from aplotly.colors import available_palettes, hex_to_rgba, rgba_to_hex, select_palette


class TestColors(TestCase):
    def test_available_palettes(self):
        self.assertEqual(available_palettes(), ["default", "greys", "night", "dark_mode"])

    def test_select_palette(self):
        for palette in available_palettes():
            output_hex_lines, output_hex_chart = select_palette(palette, "hex")
            output_rgba_lines, output_rgba_chart = select_palette(palette, "rgba")

            self.assertEqual(type(output_hex_lines), dict)
            self.assertEqual(type(output_hex_chart), dict)
            self.assertEqual(type(output_rgba_lines), dict)
            self.assertEqual(type(output_rgba_chart), dict)

            for key in ["background", "grid", "text", "axes"]:
                self.assertEqual(type(output_hex_chart[key]), str)
                self.assertEqual(type(output_rgba_chart[key]), str)

    def test_colors_palette(self):
        for palette in available_palettes():
            output_hex_lines, output_hex_chart = select_palette(palette, "hex")
            output_rgba_lines, output_rgba_chart = select_palette(palette, "rgba")

            output_hex_lines_rgba = {key: hex_to_rgba(value) for key, value in output_hex_lines.items()}
            output_hex_chart_rgba = {key: hex_to_rgba(value) for key, value in output_hex_chart.items()}

            self.assertEqual(output_hex_lines_rgba, output_rgba_lines)
            self.assertEqual(output_hex_chart_rgba, output_rgba_chart)

            output_rgba_lines_hex = {key: rgba_to_hex(value) for key, value in output_rgba_lines.items()}
            output_rgba_chart_hex = {key: rgba_to_hex(value) for key, value in output_rgba_chart.items()}

            self.assertEqual(output_rgba_lines_hex, output_hex_lines)
            self.assertEqual(output_rgba_chart_hex, output_hex_chart)


if __name__ == "__main__":
    main()
