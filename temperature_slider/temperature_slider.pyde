"""
* A slider widget to adjust the temperature, inspired by an article from @ThePracticalDev
  https://dev.to/ederchrono/making-an-animated-slider---wotw-mkj
"""

from Glyphicons import *
from Fonts import *

# Jython/processing unicode issues force me to avoid degrees symbol
#celsius = "°C"
celsius = "C"
#fahrenheit = "°F"
fahrenheit = "F"

# The range in temperature settings, F
min_temperature = 60
max_temperature = 80

# colors
white = color(255, 255, 255)
black = color(0, 0, 0)
purple = color(95, 4, 121)
pinkish_purple = color(222, 13, 177)
font_color = purple
font_highlight_color = pinkish_purple

# Allow current temp to reach target temp +/- padding.
# This also removes many restrictions and logic around size.
temperature_padding = 0.1
temperature_step = 0.01

def setup():
    size(640, 450)
    global slider
    global fan
    global fonts
    global climate_control
    global glyphs

    # instantiate our glyphicons dictionary
    glyphs = Glyphicons()

    # instantiate our fonts dictionary
    fonts = Fonts()

    climate_control = {}
    climate_control['tempRange'] = [min_temperature, max_temperature]

    # Celsius or Fahrenheit
    climate_control['use_celsius'] = False

    # default current_temperature
    climate_control['current_temperature'] = 60+random(max_temperature-min_temperature)

    # default mode
    climate_control['mode'] = None

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

    fill(font_color)
    stroke(font_color)
    line(0, ypos, xmax, ypos)
    textFont(fonts.tick_label.font)
    for i in range(10):
        x = i*xmax/10
        text("|", x, tick_mark_ypos)
        text(xpos_to_temperature_value(x, xmax, tmin, tmax), x, tick_label_ypos)
    fill(white)
    ellipse(xpos, ypos, slider_wd, slider_ht)

    # Select the appropriate glyphicon depending on slider position
    tint(black)
    if 1.0*xpos/xmax < 0.1:
        image(glyphs.temperature_low_warn, xpos-slider_wd/10, ypos-slider_ht/4)
    elif 1.0*xpos/xmax < 0.4:
        image(glyphs.temperature_low, xpos-slider_wd/10, ypos-slider_ht/4)
    elif 1.0*xpos/xmax < 0.6:
        image(glyphs.temperature, xpos-slider_wd/10, ypos-slider_ht/4)
    elif 1.0*xpos/xmax < 0.9:
        image(glyphs.temperature_high, xpos-slider_wd/10, ypos-slider_ht/4)
    else:
        image(glyphs.temperature_high_warn, xpos-slider_wd/10, ypos-slider_ht/4)
    noTint()

def draw_temperature_value(value, font, xpos, ypos, label=None):
    """Draw temperature value param."""

    textFont(font)
    fill(font_color)
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
            tint(95, 4, 121)
            image(icon_image, 0, 0)
            noTint()
            popMatrix()

    if mode == "Heating" or mode == "Cooling":
        textFont(fonts.climate_control.font)
        fill(font_color)
        text(mode, xpos, ypos)
        if mode == "Heating":
            draw_icon(glyphs.fire, 0.5, xpos*1.3, ypos*0.85) 
        elif mode == "Cooling":
            draw_icon(glyphs.snowflake, 0.5, xpos*1.3, ypos*0.85)

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
    tint(font_color)
    image(fan_img, -1.0*fan_img.width/2, -1.0*fan_img.height/2)
    noTint()
    popMatrix()

    # indicate fan status
    if fan_enabled:
        textFont(fonts.fan_label.font)
        fill(font_color)
        text("fan running", xpos-1.005*fan_wd, ypos+fan_ht)

def draw_status_item(xpos, ypos, img, img_scale=1.0, enabled=False):
    """Display the status indicator."""

    if enabled:
        pushMatrix()
        translate(xpos, ypos)
        scale(img_scale)
        tint(font_color)
        image(img, -1.0*img.width/2, -1.0*img.height/2)
        noTint()
        popMatrix()

def draw_menu_item(xpos, ypos, img, img_scale=1.0, highlight=False):
    """Display the menu item."""

    if highlight:
        tint_color = font_highlight_color
    else:
        tint_color = font_color

    pushMatrix()
    translate(xpos, ypos)
    scale(img_scale)
    tint(tint_color)
    image(img, -1.0*img.width/2, -1.0*img.height/2)
    noTint()
    popMatrix()

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
    draw_fan(fan['x'], fan['y'], fan['h'], fan['w'], glyphs.propeller, 0.5, fan['enabled'])
    update_slider(mouseX, width)
    draw_slider(slider['x'], slider['y'], slider['w'], slider['h'], width,
                                                   climate_control['tempRange'][0],
                                                   climate_control['tempRange'][1])
    draw_temperature_value(target_temperature, fonts.target_temperature.font,
                           width/2, fonts.target_temperature.size)
    draw_temperature_value(climate_control['current_temperature'], 
                           fonts.current_temperature.font,
                           width/4, fonts.target_temperature.size*0.75, "current")

    draw_status_item(0.9*width, 0.07*height, glyphs.wifi, 0.5, True)
    draw_status_item(0.9*width, 0.11*height, glyphs.bluetooth, 0.5, True)

    # draw settings menu item
    if inzone(mouseX, mouseY, 0.05*width, 0.65*height, 20, 20):
        draw_menu_item(0.05*width, 0.65*height, glyphs.cogwheels, 1.0, True)
    else:
        draw_menu_item(0.05*width, 0.65*height, glyphs.cogwheels, 1.0)

    # draw calendar menu item
    if inzone(mouseX, mouseY, 0.15*width, 0.65*height, 20, 20):
        draw_menu_item(0.15*width, 0.65*height, glyphs.calendar, 1.0, True)
    else:
        draw_menu_item(0.15*width, 0.65*height, glyphs.calendar, 1.0)

    # draw charts menu item
    if inzone(mouseX, mouseY, 0.25*width, 0.65*height, 20, 20):
        draw_menu_item(0.25*width, 0.65*height, glyphs.charts, 1.0, True)
    else:
        draw_menu_item(0.25*width, 0.65*height, glyphs.charts, 1.0)

    # draw vacation mode menu item
    if inzone(mouseX, mouseY, 0.35*width, 0.65*height, 20, 20):
        draw_menu_item(0.35*width, 0.65*height, glyphs.plane, 1.0, True)
    else:
        draw_menu_item(0.35*width, 0.65*height, glyphs.plane, 1.0)

    # draw beer mode menu item
    if inzone(mouseX, mouseY, 0.45*width, 0.65*height, 20, 20):
        draw_menu_item(0.45*width, 0.65*height, glyphs.beer, 1.0, True)
    else:
        draw_menu_item(0.45*width, 0.65*height, glyphs.beer, 1.0)
