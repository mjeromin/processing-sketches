"""
* A slider widget to adjust the temperature, inspired by an article from @ThePracticalDev
  https://dev.to/ederchrono/making-an-animated-slider---wotw-mkj
"""

# purple-ish look
font_color = (95, 4, 121)

# Download this font pack and put it in your sketch directory or your ~/.fonts/
# https://www.dafont.com/alien-encounters.font
font_name = "Alien Encounters" 

# Download GLYPHICONS FREE at http://glyphicons.com/ and install under images/glyphicons_free
# GLYPHICONS FREE are released under the Creative Commons Attribution 3.0 Unported (CC BY 3.0).
# The Full license can be found here: http://glyphicons.com/license/
glyphicons_730_temperature_image = "../images/glyphicons_free/glyphicons/png/glyphicons-730-temperature.png"
glyphicons_694_temperature_low_image = "../images/glyphicons_free/glyphicons/png/glyphicons-694-temperature-low.png"
glyphicons_695_temperature_high_image = "../images/glyphicons_free/glyphicons/png/glyphicons-695-temperature-high.png"
glyphicons_696_temperature_low_warn_image = "../images/glyphicons_free/glyphicons/png/glyphicons-696-temperature-low-warning.png"
glyphicons_697_temperature_high_warn_image = "../images/glyphicons_free/glyphicons/png/glyphicons-697-temperature-high-warning.png"
glyphicons_22_snowflake_image = "../images/glyphicons_free/glyphicons/png/glyphicons-22-snowflake.png"
glyphicons_23_fire_image = "../images/glyphicons_free/glyphicons/png/glyphicons-23-fire.png"
propeller_image = "../images/propeller.png"

# Jython/processing unicode issues force me to avoid degrees symbol
#celsius = "°C"
celsius = "C"
#fahrenheit = "°F"
fahrenheit = "F"

# The range in temperature settings, F
min_temperature = 60
max_temperature = 80

# Allow current temp to reach target temp +/- padding.
# This also removes many restrictions and logic around size.
temperature_padding = 0.1
temperature_step = 0.01


def setup():
    size(640, 450)
    global slider
    global fan
    global fonts
    global images
    global climate_control
    global white
    global black

    # convenience
    white = color(255, 255, 255)
    black = color(0, 0, 0)

    climate_control = {}
    climate_control['tempRange'] = [min_temperature, max_temperature]

    # Celsius or Fahrenheit
    climate_control['use_celsius'] = False

    # default current_temperature
    climate_control['current_temperature'] = 60+random(max_temperature-min_temperature)

    # default mode
    climate_control['mode'] = None

    fonts = {}
    fonts['color'] = color(font_color[0], font_color[1], font_color[2])
    # Create the fonts for temperature values
    fonts['slider_temperature'] = { 'font': createFont(font_name, 85), 'size': 85 }
    fonts['current_temperature'] = { 'font': createFont(font_name, 20), 'size': 20 }
    fonts['climate_control'] = { 'font': createFont(font_name, 22), 'size': 22 }
    fonts['tick_label'] = { 'font': createFont(font_name, 22), 'size': 22 }
    fonts['fan_label'] = { 'font': createFont(font_name, 12), 'size': 12 }

    images = {}
    # Download GLYPHICONS FREE at http://glyphicons.com/ and install under images/glyphicons_free
    # GLYPHICONS FREE are released under the Creative Commons Attribution 3.0 Unported (CC BY 3.0).
    # The Full license can be found here: http://glyphicons.com/license/
    images['glyphicons-730-temperature'] = loadImage(glyphicons_730_temperature_image)
    images['glyphicons-694-temperature-low'] = loadImage(glyphicons_694_temperature_low_image)
    images['glyphicons-695-temperature-high'] = loadImage(glyphicons_695_temperature_high_image)
    images['glyphicons-696-temperature-low-warn'] = loadImage(glyphicons_696_temperature_low_warn_image)
    images['glyphicons-697-temperature-high-warn'] = loadImage(glyphicons_697_temperature_high_warn_image)
    images['propeller'] = loadImage(propeller_image)
    images['glyphicons-22-snowflake'] = loadImage(glyphicons_22_snowflake_image)
    images['glyphicons-23-fire'] = loadImage(glyphicons_23_fire_image)
    
    slider = {}
    # initial position is in center of display
    slider['x'] = width/2
    slider['y'] = height/2
    # slider ellipse size
    slider['w'] = 50
    slider['h'] = 50
    # grab tracks whether the user has grabbed the slider
    slider['grab'] = False
    
    fan = {}
    # initial position
    fan['x'] = 75
    fan['y'] = 75
    # fan size
    fan['w'] = 36
    fan['h'] = 34
    fan['grab'] = False
    fan['enabled'] = False

def inzone(xpos, ypos, x, y, w, h):
    """Return True if xpos, ypos is inside the x[+/-]w,y[+/-]h zone, else return False. """

    if x-(1.0*w/2) <= xpos <= x+(1.0*w/2) and y-(1.0*h/2) <= ypos <= y+(1.0*h/2):
        return True
    else:
        return False

def xpos_to_temperature_value(xpos, xmax, tmin, tmax):
    """Return temperature associated with cool/heat relative to slider x-position. """
    return int(tmin + (tmax - tmin)*(1.0*xpos/xmax))

def xpos_to_temperature_color(xpos, xmax):
    """Return color associated with cool/heat relative to slider x-position.
    RGB values here should produce a Blue to Orange gradient.
    """
    red = 20+235*xpos/xmax
    green = 154-20*xpos/xmax
    blue = 174*(1-1.0*xpos/xmax)
    return color(red, green, blue)

def draw_slider(xpos, ypos, slider_ht, slider_wd, xmax, tmin, tmax):
    """Draw the slider widget. """

    tick_mark_ypos = ypos-0.5*slider_ht
    tick_label_ypos = ypos-slider_ht

    fill(fonts['color'])
    stroke(fonts['color'])
    line(0, ypos, xmax, ypos)
    textFont(fonts['tick_label']['font'])
    for i in range(10):
        x = i*xmax/10
        text("|", x, tick_mark_ypos)
        text(xpos_to_temperature_value(x, xmax, tmin, tmax), x, tick_label_ypos)
    fill(white)
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
    fill(fonts['color'])
    if climate_control['use_celsius']:
        if label:
            text("{} {}\n{}".format(int(value), celsius, label), xpos, ypos)
        else:
            text("{} {}".format(int(value), celsius), xpos, ypos)
    elif label:
        text("{} {}\n{}".format(int(value), fahrenheit, label), xpos, ypos)
    else:
        text("{} {}".format(int(value), fahrenheit), xpos, ypos)

def draw_climate_control_mode(mode, xpos, ypos):
    """Display the climate control mode if it is being performed"""

    def draw_icon(icon_image, icon_scale, x, y):
            pushMatrix()
            translate(x, y)
            scale(icon_scale)
            image(icon_image, 0, 0)
            popMatrix()

    if mode == "Heating" or mode == "Cooling":
        textFont(fonts['climate_control']['font'])
        fill(fonts['color'])
        text(mode, xpos, ypos)
        if mode == "Heating":
            draw_icon(images['glyphicons-23-fire'], 0.5, xpos*1.3, ypos*0.85) 
        elif mode == "Cooling":
            draw_icon(images['glyphicons-22-snowflake'], 0.5, xpos*1.3, ypos*0.85)

def draw_fan(xpos, ypos, fan_ht, fan_wd, fan_img, fan_img_scale, fan_enabled):
    """Display the fan, rotate it, and provide a user-friendly indicator."""

    pushMatrix()
    translate(xpos, ypos)
    if fan_enabled:
        angle = radians(millis()/2 % 360)
    else:
        angle = radians(0)
    rotate(angle)
    scale(fan_img_scale)
    image(fan_img, -1.0*fan_img.width/2, -1.0*fan_img.height/2)
    popMatrix()

    # indicate fan status
    if fan_enabled:
        textFont(fonts['fan_label']['font'])
        fill(fonts['color'])
        text("fan running", xpos-1.005*fan_wd, ypos+fan_ht)

def update_climate_control(target_temperature, padding=temperature_padding, step=temperature_step):
    if climate_control['current_temperature']+padding < target_temperature:
        # increase the current temperature in steps
        climate_control['current_temperature'] += step
        climate_control['mode'] = "Heating"
    elif climate_control['current_temperature']-padding > target_temperature:
        # decrease the current temperature in steps
        climate_control['current_temperature'] -= step
        climate_control['mode'] = "Cooling"
    else:
        climate_control['mode'] = None

def draw_background(mode):
    if mode == "Heating":
        bg_color = xpos_to_temperature_color(slider['x'], width)
    elif mode == "Cooling":
        bg_color = xpos_to_temperature_color(slider['x'], width)
    else:
        # default to black when climate is not changing
        bg_color = black
    background(bg_color)

def update_slider(x, xmax):
     global slider
     if slider['grab']:
        #sane limits, keep the slider in the display
        if 0 <= x <= xmax:
            slider['x'] = x
        else:
            print("slider out of bounds, ignoring update.")

def mouseReleased():
    if slider['grab']:
        slider['grab'] = False

    # toggle fan mode
    if fan['grab']:
        fan['grab'] = False
        fan['enabled'] = not fan['enabled']

def mousePressed():
    # reactive slider
    if inzone(mouseX, mouseY, slider['x'], slider['y'], slider['w'], slider['h']):
        slider['grab'] = True

    # reactive fan button
    if inzone(mouseX, mouseY, fan['x'], fan['y'], fan['w'], fan['h']):
        fan['grab'] = True

def draw():
    target_temperature = xpos_to_temperature_value(slider['x'], width,
                                                   climate_control['tempRange'][0],
                                                   climate_control['tempRange'][1])
    update_climate_control(target_temperature)
    draw_background(climate_control['mode'])
    draw_climate_control_mode(climate_control['mode'], width/2, height/4.25)
    draw_fan(fan['x'], fan['y'], fan['h'], fan['w'], images['propeller'], 0.5, fan['enabled'])
    update_slider(mouseX, width)
    draw_slider(slider['x'], slider['y'], slider['w'], slider['h'], width,
                                                   climate_control['tempRange'][0],
                                                   climate_control['tempRange'][1])
    draw_temperature_value(target_temperature, fonts['slider_temperature']['font'],
                           width/2, fonts['slider_temperature']['size'])
    draw_temperature_value(climate_control['current_temperature'], 
                           fonts['current_temperature']['font'],
                           width/4, fonts['slider_temperature']['size']*0.75, "current")
