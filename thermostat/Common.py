"""
 * A class for common processing classes
"""

# colors
white = color(255, 255, 255)
black = color(0, 0, 0)
purple = color(95, 4, 121)
pinkish_purple = color(222, 13, 177)

class Widget():
    """Widget object. Tracks position, size, and status.

    The grab flag will track whether the user has grabbed the widget.
    """

    def __init__(self, x, y, wd, ht, grab=False, enabled=True):
        self.__dict__ = {       'x': x,
                                'y': y,
                               'wd': wd,
                               'ht': ht,
                             'grab': grab,
                          'enabled': enabled
                        }

def is_inside(xpos, ypos, x, y, w, h):
    """Return True if xpos, ypos is inside the x[+/-]w,y[+/-]h zone, else return False. """

    if x-(1.0*w/2) <= xpos <= x+(1.0*w/2) and y-(1.0*h/2) <= ypos <= y+(1.0*h/2):
        return True
    else:
        return False

def draw_status_item(xpos, ypos, img, tint_color, img_scale=1.0, enabled=False):
    """Display the status indicator."""

    if enabled:
        pushMatrix()
        translate(xpos, ypos)
        scale(img_scale)
        tint(tint_color)
        image(img, -1.0*img.width/2, -1.0*img.height/2)
        noTint()
        popMatrix()

def draw_menu_item(xpos, ypos, img, tint_color, img_scale=1.0):
    """Display the menu item."""

    pushMatrix()
    translate(xpos, ypos)
    scale(img_scale)
    tint(tint_color)
    image(img, -1.0*img.width/2, -1.0*img.height/2)
    noTint()
    popMatrix()

