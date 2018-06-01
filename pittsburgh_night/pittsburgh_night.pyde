"""
 * Pittsburgh Night
"""

offset = 0
easing = 0.05

def setup():
    size(1024, 444)
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
    town_light_count = int(random(20))
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


def draw():
    global offset
    background(0)
    image(images['skyline'], 0, 0) # Display the skyline
  
    # Update the town lights
    update_town_lights()
    
    # Display town lights (if ON)
    draw_town_lights()

    # Print coordinates
    draw_coords(mouseX, mouseY)

    # Display the moon
    draw_moon()

    # Display the title
    draw_title(2*width/5, 40)

    # Display the cityscape (masking the moon)
    #image(images['cityscape'], 0, 0)
