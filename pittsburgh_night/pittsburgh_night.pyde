"""
 * Pittsburgh Night
"""

from Moon import *
from Clouds import *
from TownLights import *

moon_initial_x = 140
moon_initial_y = 84
moon_direction_x = 1
moon_direction_y = 1
moon_speed_x = 0.3
moon_speed_y = 0.0
moon_diameter = 55

max_cloud_length=120
max_cloud_height=35
min_puff_count=60
max_puff_count=95
max_puff_diameter=35

def setup():
    size(1024, 444, P3D)
    frameRate(60)
    noCursor()
    global images
    global fonts
    global town_lights
    global moon
    global clouds
    global recording

    # Disable recording flag
    recording = {}
    recording['enabled'] = False

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

    # Initialize our town lights.
    # We use x,y of the top-left building corner, then width, length of light positions
    town_lights = []
    building1_lights = TownLights(600, 273, 57, 76)
    building2_lights = TownLights(719, 283, 79, 48)
    building3_lights = TownLights(790, 242, 42, 41)

    # track each set of building lights under town_lights array
    town_lights.append(building1_lights)
    town_lights.append(building2_lights)
    town_lights.append(building3_lights)

    for i, building_lights in enumerate(town_lights):
        for light in building_lights:
            print "Generated light at ({}, {})".format(light['x'], light['y'])
        print "Generated {} lights for building #{}".format(building_lights.count(), i+1)

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

def draw_town_lights():
    """Update and display town lights if ON. """

    for building_lights in town_lights:
        building_lights.update()
        building_lights.draw()

def draw_clouds():
    # opposite direction than moon
    clouds.update(-1*moon.motion['x-direction'], moon.motion['x-speed'],
                  moon.motion['y-direction'], moon.motion['y-speed'])
    clouds.draw()

def draw():
    background(0)
    image(images['skyline'], 0, 0) # Display the skyline

    # Display town lights (if ON)
    draw_town_lights()

    # Display the moon
    moon.update_position()
    moon.draw()

    # Display the clouds
    draw_clouds()

    # Display the title
    draw_title(2*width/5, 40)

    # Print coordinates on mouse click
    if mousePressed:
        draw_coords(mouseX, mouseY)
        cursor()

    # Record output to frames when 'R' is pressed (this could take a while).
    # Stitch the frames together using PYDE tool or ffmpeg:
    #     ffmpeg -r 60 -i frames/frame-%4d.tif -pix_fmt yuv420p -r 60 frames/video.mp4
    if keyPressed and key == 'R':
        print "Recording Mode Enabled!"
        recording['enabled'] = True
    if recording['enabled']:
        saveFrame("frames/frame-####.tif")

