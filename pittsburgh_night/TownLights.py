"""
 * A class for Python Mode Processing to manage lights on buildings
"""

class TownLights(object):
    """A class to manage building lights for Python Mode Processing. """
    
    # Initialize state of lights
    # random count and placement
    def __init__(self, xpos, ypos, xlen, ylen, max_town_lights=20):
        self.lights = []
        light_count = int(random(max_town_lights)) 
        for i in range(light_count):
            x = int(xpos+random(xlen))
            y = int(ypos+random(ylen))
            light = { "x": x, "y": y,
                         "state": True, "next": millis(),
                         "image": loadImage("./images/light1.png")
                    }
            self.lights.append(light)

    def update(self, off_duration=30000, on_duration=10000):
        """Update state of town lights. """

        # Flip the state if time expired
        for light in self.lights:
            if millis() > light['next'] and light['state']:
                light['state'] = False
                light['next'] = millis() + random(on_duration)
            elif millis() > light['next']:
                light['state'] = True
                light['next'] = millis() + random(off_duration)

    def draw(self):
        """Display town lights if ON. """
        
        for light in self.lights:
            if light['state']:
                image(light['image'], light['x'], light['y'])

    def __getitem__(self, item):
        return self.lights[item] # delegate to lights.__getitem__

    def count(self):
        return len(self.lights)

