"""
 * Pittsburgh Night
"""

max_town_lights = 20
max_cloud_count = 100
min_cloud_puff_count = 70
max_cloud_puff_count = 150
max_cloud_puff_diameter = 50
max_cloud_length = 100
max_cloud_height = 20

def cloud_init():
    """Initialize our set of clouds. """
    global clouds

    # populate an index of puff colors ranked by alpha transparency
    # 0: invisible
    # 12: not very transparent
    grey_puff_colors = []
    white_puff_colors = []
    for i in range(1, 12):
        # nighttime puffs
        grey_puff_colors.append(color(200, 200, 200, i*20))

        # daytime puffs
        white_puff_colors.append(color(255, 255, 255, i*20))

    # Initialize our set of clouds
    clouds = []
    for c in range(max_cloud_count):
        cloud = {}

        # initialize each individual cloud
        cloud['shape'] = createShape(GROUP)

        # generate each puff
        for p in range(min_cloud_puff_count, int(random(min_cloud_puff_count, max_cloud_puff_count))):
            # box the puffs in
            x = random(max_cloud_length)
            y = random(max_cloud_height)

            # puffs come in a variety of colors and sizes
            d = random(max_cloud_puff_diameter)
            t = int(random(int(len(grey_puff_colors)/4)))
            noStroke()
            puff = createShape(ELLIPSE, x, y, d, d)
            puff.setFill(grey_puff_colors[t])

            # stick each puff to the cloud
            cloud['shape'].addChild(puff)

        # fix the cloud location
        cloud['x'] = random(width)
        cloud['y'] = random(height/2)
        clouds.append(cloud)

def setup():
    size(1024, 444, P3D)
    frameRate(60)
    noCursor()
    global images
    global fonts
    global town_lights
    global moon

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

    # initialize our moon position
    moon = { 'x': 140, 'y': 84,
             'x-direction': 1, 'y-direction': 1,
             'x-speed': 0.3, 'y-speed': 0.0
           }

    # Initialize our cloud(s)
    cloud_init()

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

def draw_moon():
    """Calculate position of moon and draw it. """

    # its a supermoon
    fill(255, 255, 255)

    # reset our x-position if we reach the end of the display
    if moon['x'] >= width and moon['x-direction'] > 0:
        moon['x'] = 0
    elif moon['x'] <= 0 and moon['x-direction'] < 0:
        moon['y'] = width

    # reset our y-position if we reach the end of the display
    if moon['y'] >= height and moon['y-direction'] > 0:
        moon['y'] = 0
    elif moon['y'] <= 0 and moon['y-direction'] < 0:
        moon['y'] = height

    moon['x'] += moon['x-direction'] * moon['x-speed']
    moon['y'] += moon['y-direction'] * moon['y-speed']
    ellipse(int(moon['x']), int(moon['y']), 55, 55)

def draw_clouds():
    """Calculate cloud positions and draw. """

    for cloud in clouds:
        # reset our x-position if we reach the end of the display.
        # we assume max_cloud_length to allow the cloud to float completely off screen
        if cloud['x']+max_cloud_length/2 >= width and moon['x-direction'] < 0:
            cloud['x'] = 0
        elif cloud['x']+max_cloud_length/2 <= 0 and moon['x-direction'] > 0:
            cloud['x'] = width
        cloud['x'] += -1*moon['x-direction']*moon['x-speed']
        shape(cloud['shape'], cloud['x'], cloud['y'])

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
    draw_moon()

    # Display the clouds
    draw_clouds()

    # Display the title
    draw_title(2*width/5, 40)

    # Output to frames (this could take a while).
    # Then stitch them together using ffmpeg:
    #     ffmpeg -r 60 -i frames/frame-%4d.png -pix_fmt yuv420p -r 60 frames/video.mp4
    #saveFrame("frames/frame-####.png")
