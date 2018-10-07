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
        self.__dict__ = {
                                   'temperature': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-730-temperature.png"),
                               'temperature_low': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-694-temperature-low.png"),
                              'temperature_high': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-695-temperature-high.png"),
                          'temperature_low_warn': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-696-temperature-low-warning.png"),
                         'temperature_high_warn': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-697-temperature-high-warning.png"),
                                     'snowflake': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-22-snowflake.png"),
                                          'fire': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-23-fire.png"),
                                          'wifi': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-74-wifi.png"),
                                         'plane': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-39-plane.png"),
                                        'charts': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-42-charts.png"),
                                      'calendar': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-46-calendar.png"),
                                     'cogwheels': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-138-cogwheels.png"),
                                          'beer': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-275-beer.png"),
                                     'bluetooth': loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-226-bluetooth.png"),
                                     'propeller': loadImage("../images/propeller.png")
                        }
