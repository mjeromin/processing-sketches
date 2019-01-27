# This Python file uses the following encoding: utf-8
# A class for thermostat objects.

from Glyphicons import Glyphicons
from Fonts import Font, Fonts, font_name
from Common import Widget, is_inside, draw_status_item, draw_menu_item, white, black

# unicode issues, so I'm avoiding degrees symbols for now
#celsius = "°C"
celsius = "C"
#fahrenheit = "°F"
fahrenheit = "F"

class ControlPanel():
    """ClimateControl object.

    Default range is 60-80 deg fahrenheit.
    Allow current temperature to reach target temperature in steps +/- padding.
    Initial current temperature is randomly generated within the min/max temp range.
    """

    def __init__(self, width, height, font_color, font_highlight_color, celsius=False, temp_padding=0.1, temp_step=0.01,
                 slider_temp_min=60, slider_temp_max=80, slider_wd=50, slider_ht=50,
                 fan_wd=36, fan_ht=34, fan_xpos=75, fan_ypos=75):

        self.width = width
        self.height = height
        self.temp_padding = temp_padding
        self.temp_step = temp_step
        self.slider_temp_min = slider_temp_min
        self.slider_temp_max = slider_temp_max
        self.font_color = font_color
        self.font_highlight_color = font_highlight_color

        # Initiate our glyphs
        self.glyphs = Glyphicons()

        # Initiate our fonts
        self.fonts = Fonts()

        # Celsius or Fahrenheight
        self.use_celsius = celsius

        # default current_temperature
        self.current_temperature = self.slider_temp_min + random(self.slider_temp_max - self.slider_temp_min)

        # default mode of operation
        self.mode = None

        # Initiate our temperature slider control
        # slider_wd is widget width, not to be confused with slider length (which is screen width)
        self.slider = Widget(self.width/2, self.height/2, slider_wd, slider_ht, False, True)

        # Initiate our fan control (disabled at startup)
        self.fan = Widget(fan_xpos, fan_ypos, fan_wd, fan_ht, False, False)

    def update_climate(self, setpoint):
        """Step the current temperature towards the target temperature +/- padding. Mode indicates which direction we are stepping."""

        if self.current_temperature+self.temp_padding < setpoint:
            # increase the current temperature in steps
            self.current_temperature += self.temp_step
            self.mode = "Heating"
        elif self.current_temperature-self.temp_padding > setpoint:
            # decrease the current temperature in steps
            self.current_temperature -= self.temp_step
            self.mode = "Cooling"
        else:
            self.mode = None

    def update_slider(self, mouseX):
        """Update the thermostat slider control. Enforce position between 0 and width to keep it on the display."""
        if self.slider.grab:
            if 0 <= mouseX <= self.width:
                self.slider.x = mouseX 
            else:
                print("slider out of bounds, ignoring update.")

    def xpos_to_temperature_value(self, xpos, xmax, tmin, tmax):
        """Return temperature associated with cool/heat relative to slider x-position. """
        return int(tmin + (tmax - tmin)*(1.0*xpos/xmax))
    
    def xpos_to_temperature_color(self, xpos, xmax):
        """Return color associated with cool/heat relative to slider x-position.
        RGB values here should produce a Blue to Orange gradient.
        """
        red = 20+235*xpos/xmax
        green = 154-20*xpos/xmax
        blue = 174*(1-1.0*xpos/xmax)
        return color(red, green, blue)

    def draw_background(self):
        """Draw background based on heating or cooling modes and x relative to xmax. """

        if self.mode == "Heating":
            bg_color = self.xpos_to_temperature_color(self.slider.x, self.width)
        elif self.mode == "Cooling":
            bg_color = self.xpos_to_temperature_color(self.slider.x, self.width)
        else:
            # default to black when climate is not changing
            bg_color = black
        background(bg_color)

    def mouse_released(self):
        """Function for when mouse button is released. """

        if self.slider.grab:
            self.slider.grab = False
    
        # toggle fan mode
        if self.fan.grab:
            self.fan.grab = False
            self.fan.enabled = not self.fan.enabled

    def mouse_pressed(self, mouseX, mouseY):
        """Function for when mouse button is pressed. """

        # reactive slider
        if is_inside(mouseX, mouseY, self.slider.x, self.slider.y, self.slider.wd, self.slider.ht):
            self.slider.grab = True
    
        # reactive fan button
        if is_inside(mouseX, mouseY, self.fan.x, self.fan.y, self.fan.wd, self.fan.ht):
            self.fan.grab = True

    def draw_slider(self):
        """Draw the slider widget. """
    
        xpos = self.slider.x
        ypos = self.slider.y
        height = self.slider.ht
        width = self.slider.wd
        length = self.width

        def draw_slider_tick_marks(ypos, length, height):
            """Draw tick marks, spaced by length/10."""

            font = self.fonts.tick_label.font
            tmin = self.slider_temp_min
            tmax = self.slider_temp_max
            tick_mark_ypos = ypos-0.5*height
            tick_label_ypos = ypos-height
            fill(self.font_color)
            stroke(self.font_color)
            line(0, ypos, length, ypos)
            textFont(font)
            for i in range(10):
                x = i*length/10
                text("|", x, tick_mark_ypos)
                text(self.xpos_to_temperature_value(x, length, tmin, tmax), x, tick_label_ypos)

        def draw_slider_widget(xpos, ypos, length, width, height):
            """Select appropriate glyphicon depending on slider position."""

            fill(white)
            ellipse(xpos, ypos, width, height)
            tint(black)
            if 1.0*xpos/length < 0.1:
                image(self.glyphs.temperature_low_warn, xpos-width/10,
                ypos-height/4)
            elif 1.0*xpos/length < 0.4:
                image(self.glyphs.temperature_low, xpos-width/10, ypos-height/4)
            elif 1.0*xpos/length < 0.6:
                image(self.glyphs.temperature, xpos-width/10, ypos-height/4)
            elif 1.0*xpos/length < 0.9:
                image(self.glyphs.temperature_high, xpos-width/10, ypos-height/4)
            else:
                image(self.glyphs.temperature_high_warn, xpos-width/10,
                ypos-height/4)
            noTint()

        draw_slider_tick_marks(ypos, length, height)
        draw_slider_widget(xpos, ypos, length, width, height)

    def draw_temperature_value(self, value, font, xpos, ypos, label=None):
        """Draw temperature value param."""
    
        textFont(font)
        fill(self.font_color)
        if self.use_celsius:
            if label:
                text("{} {}\n{}".format(int(value), celsius, label), xpos, ypos)
            else:
                text("{} {}".format(int(value), celsius), xpos, ypos)
        elif label:
            text("{} {}\n{}".format(int(value), fahrenheit, label), xpos, ypos)
        else:
            text("{} {}".format(int(value), fahrenheit), xpos, ypos)

    def draw_climate_control_mode(self, xpos, ypos):
        """Display the climate control mode if it is being performed"""
    
        def draw_icon(icon_image, icon_scale, x, y):
                pushMatrix()
                translate(x, y)
                scale(icon_scale)
                tint(self.font_color)
                image(icon_image, 0, 0)
                noTint()
                popMatrix()
    
        if self.mode == "Heating" or self.mode == "Cooling":
            textFont(self.fonts.climate_control.font)
            fill(self.font_color)
            text(self.mode, xpos, ypos)
            if self.mode == "Heating":
                # todo: fix these hardcoded offsets 
                draw_icon(self.glyphs.fire, 0.5, xpos*1.3, ypos*0.85) 
            elif self.mode == "Cooling":
                # todo: fix these hardcoded offsets
                draw_icon(self.glyphs.snowflake, 0.5, xpos*1.3, ypos*0.85)
            else:
                pass

    def draw_fan(self, fan_img_scale):
        """Display the fan, rotate it, and provide a user-friendly indicator."""

        xpos = self.fan.x
        ypos = self.fan.y
        height = self.fan.ht
        width = self.fan.wd
        fan_img = self.glyphs.propeller

        # Animate a spinning fan
        pushMatrix()
        translate(xpos, ypos)
        if self.fan.enabled:
            angle = radians(millis()/2 % 360)
        else:
            angle = radians(0)
        rotate(angle)
        scale(fan_img_scale)
        tint(self.font_color)
        image(fan_img, -1.0*fan_img.width/2, -1.0*fan_img.height/2)
        noTint()
        popMatrix()
    
        # indicate fan status
        if self.fan.enabled:
            textFont(self.fonts.fan_label.font)
            fill(self.font_color)
            # todo: fix hardcoded offset 
            text("fan running", xpos-1.005*width, ypos+height)

    def draw_wifi_indicator(self, xpos, ypos, scale, enabled=True):
        """Draw wifi indicator. """
        draw_status_item(xpos, ypos, self.glyphs.wifi, self.font_color, scale, enabled=True)

    def draw_bluetooth_indicator(self, xpos, ypos, scale, enable=True):
        """Draw bluetooth indicator. """
        draw_status_item(xpos, ypos, self.glyphs.bluetooth, self.font_color, scale, enabled=True)

    def draw_menu(self, mouseX, mouseY, scale=1.0):
        """Draw the control panel menu. """

        items = [self.glyphs.cogwheels,
                 self.glyphs.calendar,
                 self.glyphs.charts,
                 self.glyphs.plane,
                 self.glyphs.beer
                ]
        wfactor = 0.05
        xpos = wfactor*self.width
        ypos = 0.65*self.height
        xvar = 20
        yvar = 20
        for item in items:
            if is_inside(mouseX, mouseY, xpos, ypos, xvar, yvar):
                draw_menu_item(xpos, ypos, item, self.font_highlight_color, scale)
            else:
                draw_menu_item(xpos, ypos, item, self.font_color, scale)
            wfactor+=0.1
            xpos = wfactor*self.width

    def draw_main(self, mouseX, mouseY):
        """The main draw loop. """

        setpoint = self.xpos_to_temperature_value(self.slider.x, self.width, self.slider_temp_min, self.slider_temp_max)
        self.update_climate(setpoint)
        self.draw_background()
        self.draw_climate_control_mode(self.width/2, self.height/4.25)
        self.draw_fan(0.5)
        self.update_slider(mouseX)
        self.draw_slider()
        self.draw_temperature_value(setpoint, self.fonts.setpoint.font, self.width/2, self.fonts.setpoint.size)
        self.draw_temperature_value(self.current_temperature, self.fonts.current_temperature.font, self.width/4, self.fonts.setpoint.size*0.75, "current")
        self.draw_wifi_indicator(0.9*self.width, 0.07*self.height, 0.5)
        self.draw_bluetooth_indicator(0.9*self.width, 0.11*self.height, 0.5)
        self.draw_menu(mouseX, mouseY)

