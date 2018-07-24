"""
* A slider widget to adjust the temperature, inspired by an article from @ThePracticalDev
  https://dev.to/ederchrono/making-an-animated-slider---wotw-mkj
"""

# Jython/processing unicode issues force me to avoid degrees symbol
#celsius = "°C"
celsius = "C"
#fahrenheit = "°F"
fahrenheit = "F"

def setup():
    size(640, 640)
    global tempRange
    global slider
    global fonts
    global use_celsius

    # The range in temperature settings, F
    tempRange = [60, 80]

    # Celsius or Fahrenheit
    use_celsius = False

    fonts = {}
    # Download these font packs and put them in your sketch directory or your ~/.fonts/
    # https://www.dafont.com/monofur.font
    # Create the fonts for temperature values
    fonts['temperature'] = { 'font': createFont("monofur", 95), 'size': 95 }
    fonts['tick_label'] = { 'font': createFont("monofur", 22), 'size': 22 }
    
    slider = {}
    slider['x'] = width/2
    slider['y'] = height/2
    slider['w'] = 50
    slider['h'] = 50
    slider['grab'] = False

def inzone(xpos, ypos, x, y, w, h):
    """Return True if xpos, ypos is inside the x,y,w,h zone, else return False. """

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

    # draw widget shape (ie. circle with icon)
    line(0, slider['y'], width, slider['y'])
    textFont(fonts['tick_label']['font'])
    fill(0, 0, 0)
    for i in range(10):
        x = i*width/10
        text("|", x, slider['y']-10)
        text(xpos_to_temperature_value(x, width), x, slider['y']-30)
    fill(255, 255, 255)
    ellipse(slider['x'], slider['y'], slider['w'], slider['h'])

def draw_temperature_value(value):
    """Draw temperature value param."""

    textFont(fonts['temperature']['font'])
    fill(255, 255, 255)
    if use_celsius:
        text("{} {}".format(value, celsius), width/2, fonts['temperature']['size'])
    else:
        text("{} {}".format(value, fahrenheit), width/2, fonts['temperature']['size'])

def draw():
    temperature = xpos_to_temperature_value(slider['x'], width)
    print("Temperature: {}".format(temperature))
    bg_color = xpos_to_temperature_color(slider['x'], width)
    background(bg_color)
    draw_slider()
    draw_temperature_value(temperature)
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
