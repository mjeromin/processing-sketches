"""
 * A class for our fonts dictionary, for use with Processing in Python mode
"""

# Download this font pack and put it in your sketch directory or your ~/.fonts/
# https://www.dafont.com/alien-encounters.font
font_name = "Alien Encounters"

class Font(object):
    def __init__(self, d):
        self.__dict__ = d

class Fonts(object):
    """Store a dictionary of fonts."""

    def __init__(self, d=None):
        d = {}
        d['target_temperature'] = Font({ 'font': createFont(font_name, 85), 'size': 85 })
        d['current_temperature'] = Font({ 'font': createFont(font_name, 20), 'size': 20 })
        d['climate_control'] = Font({ 'font': createFont(font_name, 22), 'size': 22 })
        d['tick_label'] = Font({ 'font': createFont(font_name, 22), 'size': 22 })
        d['fan_label'] = Font({ 'font': createFont(font_name, 12), 'size': 12 })
        self.__dict__ = d
