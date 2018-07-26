"""
* A slider widget to adjust the temperature, inspired by an article from @ThePracticalDev
  https://dev.to/ederchrono/making-an-animated-slider---wotw-mkj
"""

# Jython/processing unicode issues force me to avoid degrees symbol
#celsius = "°C"
celsius = "C"
#fahrenheit = "°F"
fahrenheit = "F"

temperature_padding = 0.1
temperature_step = 0.01

def setup():
    size(640, 640)
    global tempRange
    global slider
    global fonts
    global images
    global use_celsius
    global current_temperature

    # The range in temperature settings, F
    tempRange = [60, 80]

    # Celsius or Fahrenheit
    use_celsius = False

    # default current_temperature
    current_temperature = 60+random(tempRange[1]-tempRange[0])

    fonts = {}
    # Download these font packs and put them in your sketch directory or your ~/.fonts/
    # https://www.dafont.com/monofur.font
    # Create the fonts for temperature values
    fonts['slider_temperature'] = { 'font': createFont("monofur", 85), 'size': 85 }
    fonts['current_temperature'] = { 'font': createFont("monofur", 20), 'size': 20 }
    fonts['climate_control'] = { 'font': createFont("monofur", 22), 'size': 22 }
    fonts['tick_label'] = { 'font': createFont("monofur", 22), 'size': 22 }

    images = {}
    # Download GLYPHICONS FREE at http://glyphicons.com/ and install under images/glyphicons_free
    # GLYPHICONS FREE are released under the Creative Commons Attribution 3.0 Unported (CC BY 3.0).
    # The Full license can be found here: http://glyphicons.com/license/
    images['glyphicons-730-temperature'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-730-temperature.png")
    images['glyphicons-694-temperature-low'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-694-temperature-low.png")
    images['glyphicons-695-temperature-high'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-695-temperature-high.png")
    images['glyphicons-696-temperature-low-warn'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-696-temperature-low-warning.png")
    images['glyphicons-697-temperature-high-warn'] = loadImage("../images/glyphicons_free/glyphicons/png/glyphicons-697-temperature-high-warning.png")
    
    slider = {}
    # initial position is in center of display
    slider['x'] = width/2
    slider['y'] = height/2
    # slider ellipse size
    slider['w'] = 50
    slider['h'] = 50
    # grab tracks whether the user has grabbed the slider
    slider['grab'] = False

def inzone(xpos, ypos, x, y, w, h):
    """Return True if xpos, ypos is inside the x[+/-]w,y[+/-]h zone, else return False. """

    if x-(1.0*w/2) <= xpos <= x+(1.0*w/2) and y-(1.0*h/2) <= ypos <= y+(1.0*h/2):
        return True
    else:
        return False

def xpos_to_temperature_value(xpos, xmax):
    """Return temperature associated with cool/heat relative to slider x-position. """
    return int(tempRange[0] + (tempRange[1] - tempRange[0])*(1.0*xpos/xmax))

def xpos_to_temperature_color(xpos, xmax):
    """Return color associated with cool/heat relative to slider x-position.
    RGB values here should produce a Blue to Orange gradient.
    """
    red = 20+235*xpos/xmax
    green = 154-20*xpos/xmax
    blue = 174*(1-1.0*xpos/xmax)
    return color(red, green, blue)

def draw_slider(xpos, ypos, slider_ht, slider_wd, xmax):
    """Draw the slider widget. """

    tick_mark_ypos = ypos-0.5*slider_ht
    tick_label_ypos = ypos-slider_ht

    fill(95, 4, 121)
    stroke(95, 4, 121)
    line(0, ypos, xmax, ypos)
    textFont(fonts['tick_label']['font'])
    for i in range(10):
        x = i*xmax/10
        text("|", x, tick_mark_ypos)
        text(xpos_to_temperature_value(x, xmax), x, tick_label_ypos)
    fill(255, 255, 255)
    ellipse(xpos, ypos, slider_wd, slider_ht)

    # Select the appropriate glyphicon depending on slider position
    if 1.0*xpos/xmax < 0.1:
        image(images['glyphicons-696-temperature-low-warn'], xpos-slider_wd/10, ypos-slider_ht/4)
    elif 1.0*xpos/xmax < 0.4:
        image(images['glyphicons-694-temperature-low'], xpos-slider_wd/10, ypos-slider_ht/4)
    elif 1.0*xpos/xmax < 0.6:
        image(images['glyphicons-730-temperature'], xpos-slider_wd/10, ypos-slider_ht/4)
    elif 1.0*xpos/xmax < 0.9:
        image(images['glyphicons-695-temperature-high'], xpos-slider_wd/10, ypos-slider_ht/4)
    else:
        image(images['glyphicons-697-temperature-high-warn'], xpos-slider_wd/10, ypos-slider_ht/4)

def draw_temperature_value(value, font, xpos, ypos, label=None):
    """Draw temperature value param."""

    textFont(font)
    fill(95, 4, 121)
    if use_celsius:
        if label:
            text("{} {}\n{}".format(int(value), celsius, label), xpos, ypos)
        else:
            text("{} {}".format(int(value), celsius), xpos, ypos)
    elif label:
        text("{} {}\n{}".format(int(value), fahrenheit, label), xpos, ypos)
    else:
        text("{} {}".format(int(value), fahrenheit), xpos, ypos)

def draw_climate_control_operation(climate_control):
    """Display the climate control operation if it is being performed"""

    if climate_control:
        textFont(fonts['climate_control']['font'])
        fill(95, 4, 121)
        text(climate_control, width/2, height/4 - 50)

def draw():
    global current_temperature
    climate_control = None
    temperature = xpos_to_temperature_value(slider['x'], width)
    if current_temperature+temperature_padding < temperature:
        # increase the current temperature in steps
        current_temperature += temperature_step
        bg_color = xpos_to_temperature_color(slider['x'], width)
        background(bg_color)
        draw_climate_control_operation("Heating")
    elif current_temperature-temperature_padding > temperature:
        # decrease the current temperature in steps
        current_temperature -= temperature_step
        bg_color = xpos_to_temperature_color(slider['x'], width)
        background(bg_color)
        draw_climate_control_operation("Cooling")
    else:
        # default to black when climate is not changing
        bg_color = color(0, 0, 0)
        background(bg_color)
    draw_slider(slider['x'], slider['y'], slider['w'], slider['h'], width)
    draw_temperature_value(temperature, fonts['slider_temperature']['font'],
                           width/2, fonts['slider_temperature']['size'])
    draw_temperature_value(current_temperature, fonts['current_temperature']['font'],
                           width/4, fonts['slider_temperature']['size']*0.75, "current")
    if mousePressed and inzone(mouseX, mouseY,
                               slider['x'], slider['y'],
                               slider['w'], slider['h']):
        slider['grab'] = True
    elif not mousePressed:
        slider['grab'] = False
    if slider['grab']:
        #sane limits, keep the slider in the display
        if 0 <= mouseX <= width:
            slider['x'] = mouseX
            print("slider set to ({},{}), temperature {}".format(slider['x'],
                                                                 slider['y'],
                                                                 temperature))
        else:
            print("slider out of bounds, ignoring update.")
