"""
* A circle avatar with a sight that follows the mouse. On mouse click it fires a laser.
"""

from collections import defaultdict
from java.awt.event import KeyEvent
from java.lang.reflect import Modifier


def setup():
    size(640, 640)
    global colors
    global bobble
    global position
    global key_names

    key_names = defaultdict(lambda: 'UNKNOWN')
    for f in KeyEvent.getDeclaredFields():
        if Modifier.isStatic(f.getModifiers()):
            name = f.getName()
            if name.startswith("VK_"):
                key_names[f.getInt(None)] = name[3:]
            
    position = {}
    position['x'] = width/2
    position['y'] = height/2
    
    colors = {}
    colors['white'] = color(255, 255, 255)
    colors['blueish'] = color(39, 61, 183)
    colors['redish'] = color(211, 17, 24)

    # initialize our avatar shape
    d = 55
    bobble = createShape(GROUP)  
    bubble = createShape(ELLIPSE, 0, 0, d, d)
    bubble.setFill(colors['blueish'])
    bobble.noStroke()
    bobble.addChild(bubble)
    sight = createShape()
    sight.beginShape()
    sight.vertex(0, 0)
    sight.vertex(d/2, -d/2)
    # correction of 45 deg
    sight.rotate(radians(45))
    sight.endShape(CLOSE)
    bobble.addChild(sight)

def draw():
    background(colors['white'])

    pushMatrix()  
    # center our rotation to the center of the sketch
    #x0 = width/2
    #y0 = height/2
    x0 = position['x']
    y0 = position['y']
    translate(x0, y0)

    # rotate around the center
    angle = atan2(mouseY - y0, mouseX - x0)
    rotate(angle)

    # Draw our bobble at the center of the rotation
    shape(bobble, 0, 0)
    popMatrix()
    
    # laser beams
    # fire laser on mouse press
    if mousePressed:
        stroke(colors['redish'])
        line(x0, y0, mouseX, mouseY)

def keyPressed():
    # Move avatar
    if key == CODED and key_names[keyCode] == "RIGHT":
        position['x'] += 1
        print "New position({}, {})".format(position['x'], position['y'])
    elif key == CODED and key_names[keyCode] == "LEFT":
        position['x'] -= 1
        print "New position({}, {})".format(position['x'], position['y'])
    elif key == CODED and key_names[keyCode] == "DOWN":
        position['y'] += 1
        print "New position({}, {})".format(position['x'], position['y'])
    elif key == CODED and key_names[keyCode] == "UP":
        position['y'] -= 1
        print "New position({}, {})".format(position['x'], position['y'])
    elif key == CODED:
        print "Unbound keycode {}".format(key_names[keyCode])
    else:
        print "Unbound key {}".format(str(key))
