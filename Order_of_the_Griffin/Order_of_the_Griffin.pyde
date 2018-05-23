"""
 * Testing out a Dungeon Explorer Menu with Mouse interaction
"""

offset = 0
easing = 0.05

def setup():
    size(956, 718)
    global img
    # load screenshot from D&D: Order of the Griffin
    img = loadImage("https://3.bp.blogspot.com/-fjOGTuCp8a8/WXQ3AxZWQNI/AAAAAAAACpY/UkQatd0xDOk_odLnOvyQwDshmSTAeHY2QCLcBGAs/s1600/screen03412.bmp")    # Load an image into the program
    
    # Download this font and put it in the sketch directory or your ~/.fonts/
    # https://www.dafont.com/dungeon-sn.font
    # Create this font
    f = createFont("dungeon", 24)
    textFont(f)


def draw():
    global offset
    image(img, 0, 0)    # Display at full opacity

    # Mask away this part of the image so we have a clean canvas
    fill(73, 145, 219)
    noStroke()
    rect(0, 0, 287, 312) # text background blue
    
    # Insert our new menu
    fill(255, 255, 255)
    text("BUY  A  DRINK", 0, 47, -32)
    text("START  A  FIRE", 0, 95, -32)
    text("BURP", 0, 138, -32)
    textSize(32)
    text("CARVE  INITIALS  IN  TABLE", 0, 186, -32)
    textSize(35)
    text("GET  A  ROOM", 0, 234, -32)
    text("LEAVE", 0, 282, -32)
    # The menu will highlight the item your mouse hovers over
    if mouseX <= 287:
        if mouseY <= 47:
            fill(146,181,255)
            rect(0, 20, 287, 20)
            fill(218, 148, 1)
            text("BUY  A  DRINK", 0, 47, -32)
        elif mouseY <= 95:
            fill(146,181,255)
            rect(0, 70, 287, 19)
            fill(218, 148, 1)
            text("START  A  FIRE", 0, 95, -32)
        elif mouseY <= 138:
            fill(146,181,255)
            rect(0, 112, 287, 19)
            fill(218, 148, 1)
            text("BURP", 0, 138, -32)
        elif mouseY <= 186:
            fill(146,181,255)
            rect(0, 162, 287, 19)
            fill(218, 148, 1)
            textSize(32)
            text("CARVE  INITIALS  IN  TABLE", 0, 186, -32)
            textSize(35)
        elif mouseY <= 234:
            fill(146,181,255)
            rect(0, 209, 287, 19)
            fill(218, 148, 1)
            text("GET  A  ROOM", 0, 234, -32)
        elif mouseY <= 282:
            fill(146,181,255)
            rect(0, 256, 287, 19)
            fill(218, 148, 1)
            text("LEAVE", 0, 282, -32)
