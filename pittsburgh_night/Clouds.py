"""
 * Clouds classes for Python Mode Processing 
"""

class CloudColors(object):
    """A list of cloud colors ranked by alpha transparency. """

    def __init__(self, nighttime=True):
        # 0: invisible
        # 4: somewhat transparent
        # 12: not very transparent
        self.colors = []
        for i in range(4):
            if nighttime:
                self.colors.append(color(200, 200, 200, i*20))
            else:
                self.colors.append(color(255, 255, 255, i*20))

    def __getitem__(self, item):
        return self.colors[item] # delegate to colors.__getitem__

    def count(self):
        return len(self.colors)

class Cloud(object):
    """An individual cloud. """

    # override these defaults during instantiation
    def __init__(self, max_cloud_length=100, max_cloud_height=20,
                       min_puff_count=30, max_puff_count=75,
                       max_puff_diameter=50, nighttime=True):

        # initialize our puff colors
        puff_colors = CloudColors(nighttime)

        # initialize our cloud shape
        self.shape = createShape(GROUP)

        # box the puffs in
        self.length = random(max_cloud_length)
        self.height = random(max_cloud_height)

        # generate each puff
        self.puff_count = int(random(min_puff_count, max_puff_count))
        for p in range(self.puff_count):
            # puffs come in a variety of colors and sizes
            x = random(self.length)
            y = random(self.height)
            d = int(random(max_puff_diameter))
            c = int(random(puff_colors.count()))
            noStroke()
            puff = createShape(ELLIPSE, x, y, d, d)
            puff.setFill(puff_colors[c])

            # stick each puff to the cloud
            self.shape.addChild(puff)

        # fix the cloud location, height biased towards the top
        self.x = random(width)
        self.y = random(height/2)

    def update(self, x_direction, x_speed, y_direction, y_speed):
        """Calculate cloud positions after one step.
        Assuming direction is either -1 (moving left) or 1 (moving right).
        """

        # reset our x-position if we reach the end of the display.
        # we leave some room for cloud_length so it can float completely off screen
        if self.x+self.length/2 >= width and x_direction > 0:
            self.x = 0
        elif self.x+self.length/2 <= 0 and x_direction < 0:
            self.x = width
        self.x += x_direction * x_speed

        # reset our y-position if we reach the end of the display.
        # we leave some room for cloud_height so it can float completely off screen
        if self.y+self.height/2 >= height and y_direction > 0:
            self.y = 0
        elif self.y+self.height/2 <= 0 and y_direction < 0:
            self.y = height
        self.y += y_direction * y_speed

    def draw(self):
        """Draw our cloud. """

        shape(self.shape, self.x, self.y)

    def show_length(self):
        return self.length

    def show_height(self):
        return self.height

    def show_puff_count(self):
        return self.puff_count

    def show_position(self):
        return (self.x, self.y)

class Clouds(object):
    """Initialize a set of clouds. """

    def __init__(self, max_cloud_count=130):
        self.clouds = []
        for c in range(max_cloud_count):
            cloud = Cloud()
            print "Generated cloud: length[{}], height[{}], puffs[{}], ({})".format(
                cloud.show_length(),
                cloud.show_height(),
                cloud.show_puff_count(),
                cloud.show_position())
            self.clouds.append(cloud)

    def update(self, x_direction, x_speed, y_direction, y_speed):
        """Calculate cloud positions after one step. """

        for cloud in self.clouds:
            cloud.update(x_direction, x_speed, y_direction, y_speed)

    def draw(self):
        """Draw our clouds. """

        for cloud in self.clouds:
            cloud.draw()

    def __getitem__(self, item):
        return self.clouds[item] # delegate to clouds.__getitem__

    def count(self):
        return len(self.clouds)
