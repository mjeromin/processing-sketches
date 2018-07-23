"""
* A slider widget to adjust the temperature, inspired by an article from @ThePracticalDev
  https://dev.to/ederchrono/making-an-animated-slider---wotw-mkj
"""

# from colors import white

def setup():
    size(640, 640)
    global colors
    global tempRange
    global slider

    tempRange = [10, 20]

    # colors = Colors()
    colors = {}
    colors['white'] = color(255, 255, 255)
    
    slider = {}
    slider['x'] = width/2
    slider['y'] = height/2
    slider['w'] = 50
    slider['h'] = 50
    slider['grab'] = False

def inzone(xpos, ypos, x, y, w, h):
    # return True/False
    if x-(1.0*w/2) <= xpos <= x+(1.0*w/2) and y-(1.0*h/2) <= ypos <= y+(1.0*h/2):
        return True
    else:
        return False

def xpos_to_temperature_value(xpos, width):
    """Return temperature associated with cool/heat. """
    return int(tempRange[0] + (tempRange[1] - tempRange[0])*(1.0*xpos/width))

def xpos_to_temperature_color(xpos, width):
    """Return color associated with cool/heat. Blue to Orange gradient-ish."""
    red = 20+235*xpos/width
    green = 154-20*xpos/width
    blue = 174*(1-1.0*xpos/width)
    return color(red, green, blue)

def draw_slider():
    """Draw the slider widget. """
    
    # draw line (0,width)
    # draw tick marks, mark=width/10, font numbers
    # draw widget shape (ie. circle with icon)
    ellipse(slider['x'], slider['y'], slider['w'], slider['h'])
          
def draw():
    temperature = xpos_to_temperature_value(slider['x'], width)
    print("Temperature: {}".format(temperature))
    bg_color = xpos_to_temperature_color(slider['x'], width)
    background(bg_color)
    draw_slider()
    if mousePressed and inzone(mouseX, mouseY,
                               slider['x'], slider['y'],
                               slider['w'], slider['h']):
        slider['grab'] = True
        print("mousePressed and InZone, grabbing slider at ({},{})".format(mouseX,mouseY))
    elif not mousePressed:
        slider['grab'] = False
        print("mouseNotPressed, slider at ({},{})".format(slider['x'],slider['y']))
    if slider['grab']:
        #sane limits, keep the slider in the display
        if 0 <= mouseX <= width:
            slider['x'] = mouseX
            print("slider set to ({},{})".format(slider['x'],slider['y']))
        else:
            print("slider out of bounds, ignoring update.")
