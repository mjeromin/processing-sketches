"""
 * Pittsburgh Night
"""

from Moon import *
from Clouds import * 

max_town_lights = 20
max_cloud_count = 100
moon_initial_x = 140
moon_initial_y = 84
moon_direction_x = 1
moon_direction_y = 1
moon_speed_x = 0.3
moon_speed_y = 0.0
moon_diameter = 55

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
