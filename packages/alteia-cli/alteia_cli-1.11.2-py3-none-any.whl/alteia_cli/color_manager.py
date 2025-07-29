import colorsys
import hashlib


class UniqueColor:
    # Ensure for a given string to always get the same color
    def __init__(self):
        self.colored = {}
        self.colors_used = []
        self.saturation = 0.7
        self.luminosity = 0.6

    def _get_hue(self, to_color: str):
        # This is fun : we get the hash from md5, grab only the first byte part,
        # modulo it with 256 to get a range of 0-255, and divide it to get 0-1
        # So, for a given string, we have always the same hue
        return float((hashlib.md5(to_color.encode("utf-8")).digest()[0] % 256) / 256)

    def _generate_color(self, to_color: str, try_nb: int = 0):
        raw_hue = self._get_hue(to_color=to_color)
        result_color = tuple(int(x * 255) for x in colorsys.hls_to_rgb(raw_hue, l=self.luminosity, s=self.saturation))

        if result_color not in self.colors_used:
            self.colors_used.append(result_color)
        else:
            if try_nb < 10:
                result_color = self._generate_color(try_nb=try_nb + 1, to_color=to_color)

        return result_color

    def get_colored(self, to_color: str):
        if to_color in self.colored:
            result_color = self.colored[to_color]
        else:
            result_color = self._generate_color(to_color=to_color)
            self.colored[to_color] = result_color

        return result_color
