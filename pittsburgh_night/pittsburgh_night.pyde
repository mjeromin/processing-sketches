"""
 * Pittsburgh Night
"""

from Moon import *

max_town_lights = 20
max_cloud_count = 100
moon_initial_x = 140
moon_initial_y = 84
moon_direction_x = 1
moon_direction_y = 1
moon_speed_x = 0.3
moon_speed_y = 0.0
moon_diameter = 55

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

def setup():
    size(1024, 444, P3D)
    frameRate(60)
    noCursor()
    global images
    global fonts
    global town_lights
    global moon
    global clouds

    # load image of downtown Pittsburgh at night (phone camera)
    images = {}
    images['skyline'] = loadImage("./images/pittsburgh_night.png")

    # Uncomment the following line to see the available fonts
    #print PFont.list();

    fonts = {}
    # Download these font packs and put them in your sketch directory or your ~/.fonts/
    # https://www.dafont.com/monofur.font
    # https://www.dafont.com/hamburger-heaven.font
    # Create the fonts for the coordinates and title
    fonts['coords'] = createFont("monofur", 12)
    fonts['title'] = createFont("HamburgerHeaven", 42)

    # Initialize state of lights
    # random count and placement along building #1
    town_lights = []
    town_light_count = int(random(max_town_lights))
    print "producing {} lights for building #1".format(town_light_count)
    for i in range(town_light_count):
        x = int(600+random(57))
        y = int(273+random(76))
        print "producing light at ({},{})".format(x,y)
        light = { "x": x, "y": y,
                     "state": True, "next": millis(),
                     "image": loadImage("./images/light1.png")
                }
        town_lights.append(light)

    # initialize our moon
    moon = Moon(moon_initial_x, moon_initial_y,
                moon_direction_x, moon_direction_y,
                moon_speed_x, moon_speed_y, moon_diameter)

    # Initialize our cloud(s)
    clouds = Clouds()
    print "Generated {} clouds.".format(clouds.count())

def draw_coords(x, y):
    textFont(fonts['coords'])
    fill(255, 255, 255)
    text("({}, {})".format(str(x),str(y)), 10, 10)

def draw_title(x, y):
    textFont(fonts['title'])
    fill(240, 174, 0)
    text("Pittsburgh", x, y)

def update_town_lights():
    """Update state of town lights. """

    # Flip the state if time expired
    for light in town_lights:
        if millis() > light['next'] and light['state']:
            light['state'] = False
            light['next'] = millis() + random(10000)
        elif millis() > light['next']:
            light['state'] = True
            light['next'] = millis() + random(30000)

def draw_town_lights():
    """Display town lights if ON. """

    for light in town_lights:
        if light['state']:
            image(light['image'], light['x'], light['y'])

def draw_clouds():
    """Calculate cloud positions and draw. """

    # opposite direction than moon
    clouds.update(-1*moon.motion['x-direction'], moon.motion['x-speed'],
                  moon.motion['y-direction'], moon.motion['y-speed'])
    clouds.draw()

def draw():
    background(0)
    image(images['skyline'], 0, 0) # Display the skyline

    # Update the town lights
    update_town_lights()

    # Display town lights (if ON)
    draw_town_lights()

    # Print coordinates on mouse click
    if mousePressed:
        draw_coords(mouseX, mouseY)
        cursor(CROSS)

    # Display the moon
    moon.update_position()
    moon.draw()

    # Display the clouds
    draw_clouds()

    # Display the title
    draw_title(2*width/5, 40)

    # Output to frames (this could take a while).
    # Then stitch them together using ffmpeg:
    #     ffmpeg -r 60 -i frames/frame-%4d.png -pix_fmt yuv420p -r 60 frames/video.mp4
    #saveFrame("frames/frame-####.png")
