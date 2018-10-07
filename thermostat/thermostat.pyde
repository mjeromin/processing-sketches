"""
* A Thermostat UI, inspired by an article from @ThePracticalDev
  https://dev.to/ederchrono/making-an-animated-slider---wotw-mkj
"""

from Thermostat import ControlPanel
from Common import purple, pinkish_purple

# colors
font_color = purple
font_highlight_color = pinkish_purple

def setup():
    size(640, 450)
    global control_panel

    # create our thermostat object
    control_panel = ControlPanel(width, height, font_color, font_highlight_color)

def mouseReleased():
    control_panel.mouse_released()

def mousePressed():
    control_panel.mouse_pressed(mouseX, mouseY)

def draw():
    control_panel.draw_main(mouseX, mouseY)
