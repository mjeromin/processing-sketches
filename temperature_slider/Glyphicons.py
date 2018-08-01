"""
 * A class for our images dictionary, for use with Processing in Python mode
 * Download GLYPHICONS FREE at http://glyphicons.com/ and install under
 * ../images/glyphicons_free
 *
 * GLYPHICONS FREE are released under the Creative Commons Attribution 3.0 Unported (CC BY 3.0).
 * The Full license can be found here: http://glyphicons.com/license/
 *
 * Note: To apply tint(), glyphicons will need to be inverted from black to white.
 *       With ImageMajick, we can invert using this command: `convert -negate image_black.png image_white.png`
"""

class Glyphicons(object):
    """Store a dictionary of glyphicons."""

    def __init__(self):
        d = {}
        d['temperature'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-730-temperature.png")
        d['temperature_low'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-694-temperature-low.png")
        d['temperature_high'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-695-temperature-high.png")
        d['temperature_low_warn'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-696-temperature-low-warning.png")
        d['temperature_high_warn'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-697-temperature-high-warning.png")
        d['snowflake'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-22-snowflake.png")
        d['fire'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-23-fire.png")
        d['wifi'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-74-wifi.png")
        d['plane'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-39-plane.png")
        d['charts'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-42-charts.png")
        d['calendar'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-46-calendar.png")
        d['cogwheels'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-138-cogwheels.png")
        d['beer'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-275-beer.png")
        d['bluetooth'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-226-bluetooth.png")
        d['propeller'] = loadImage("../images/propeller.png")
        self.__dict__ = d
