"""
* A slider widget to adjust the temperature, inspired by an article from @ThePracticalDev
  https://dev.to/ederchrono/making-an-animated-slider---wotw-mkj
"""

# from colors import white

def setup():
    size(640, 640)
    global colors
    global tempRange
    global sliderX
    global sliderY
    global sliderW
    global sliderH
    global sliderGrab

    tempRange = [10, 20]

    # colors = Colors()
    colors = {}
    colors['white'] = color(255, 255, 255)
    
    sliderX = mouseX
    sliderY = 0 # constant
    sliderW = 10 # constant
    sliderH = 10 # constant
    sliderGrab = False

def inzone(x, y, w, h):
    # return True/False
    pass

def xpos_to_temperature_value(xpos, width):
    """Return temperature associated with cool/heat. """
    return int(tempRange[0] + (tempRange[1] - tempRange[0])*(1.0*xpos/width))

def xpos_to_temperature_color(xpos, width):
    """Return color associated with cool/heat. Blue to Orange gradient-ish."""
    red = 20+235*xpos/width
    green = 154-20*xpos/width
    blue = 174*(1-1.0*xpos/width)
    return color(red, green, blue)

def draw_slider(x):
    # draw line (0,width)
    # draw tick marks, mark=width/10, font numbers
    # draw widget shape (ie. circle with icon)
    pass

def draw():
    temperature = xpos_to_temperature_value(mouseX, width)
    print("Temperature: {}".format(temperature))
    bg_color = xpos_to_temperature_color(mouseX, width)
    background(bg_color)
    #draw_slider(sliderX)
    #if mousePressed and inzone(sliderX, sliderY, sliderW, sliderH):
    #    sliderGrab = True
    #elif not mousePressed:
    #    sliderGrab = False
    #if sliderGrab:
    #    sliderX = mouseX
