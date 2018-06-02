"""
 * A Moon class for Python Mode Processing 
"""

class Moon(object):
    def __init__(self, x, y, xdir, ydir, xspeed, yspeed, diameter, load_image=True):
        self.motion = {}
        self.motion['x'] = x
        self.motion['y'] = y
        self.motion['x-direction'] = xdir
        self.motion['y-direction'] = ydir
        self.motion['x-speed'] = xspeed
        self.motion['y-speed'] = yspeed

        # it's a supermoon!
        self.color = color(255, 255, 255)

        # shape
        self.size = diameter

        # image
        # assuming the file is packed with the class
        if load_image:
            self.image = loadImage("./images/moon.png")
        else:
            self.image = None

    def update_position(self):
        """Calculate our new position. """

        # reset our x-position if we reach the end of the display
        if self.motion['x'] >= width and self.motion['x-direction'] > 0:
            self.motion['x'] = 0
        elif self.motion['x'] <= 0 and self.motion['x-direction'] < 0:
            self.motion['y'] = width

        # reset our y-position if we reach the end of the display
        if self.motion['y'] >= height and self.motion['y-direction'] > 0:
            self.motion['y'] = 0
        elif self.motion['y'] <= 0 and self.motion['y-direction'] < 0:
            self.motion['y'] = height

        self.motion['x'] += self.motion['x-direction'] * self.motion['x-speed']
        self.motion['y'] += self.motion['y-direction'] * self.motion['y-speed']

    def draw(self):
        if self.image:
            pushMatrix()
            # hardcoded scale factor...we should come back to this
            scale_factor = 0.3
            scale(scale_factor)
            image(self.image, self.motion['x']/scale_factor, self.motion['y']/scale_factor)
            popMatrix()
        else:
            fill(self.color)
            ellipse(int(self.motion['x']), int(self.motion['y']), self.size, self.size)

