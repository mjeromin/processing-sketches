"""
Hello World
"""

def setup():
    size(640, 360)
    # Create the font using Monofur
    # https://www.dafont.com/monofur.font
    textFont(createFont("Monofur", 36))

def draw():
    background(0)  # Set background to black
    # Draw the letter to the center of the screen
    textSize(14)
    text("Hello World!", 50, 50)
