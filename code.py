# My Godzilla Hat Code - @alt_bier
from adafruit_circuitplayground.express import cpx
import random

#cpx.pixels.brightness = 0.5 # 50 pct
cpx.pixels.fill((0, 0, 0))  # Turn off the NeoPixels if they're on!

# Function to give us a nice color swirl on the built in NeoPixel (R,G,B)
def wheeln(pos, sft):
    if (pos + sft) > 255:
        pos = (pos + sft) - 256
    else:
        pos = (pos + sft)
    if (pos < 0) or (pos > 255):
        return (0, 0, 0)
    if pos < 85:
        return (int(255 - pos*3), int(pos*3), 0)
    elif pos < 170:
        pos -= 85
        return (0, int(255 - (pos*3)), int(pos*3))
    else:
        pos -= 170
        return (int(pos*3), 0, int(255 - pos*3))

# Function to flash random colors
def randcolor():
    randgr = randrd = randbl = 0
    # determine if all colors off
    if (random.randint(0,14) == 1):
        # if on then determine if each color is off and return an intensity value if on
        if (random.randint(0,1) == 1):
            randgr = random.randint(1,255)
        if (random.randint(0,1) == 1):
            randrd = random.randint(1,255)
        if (random.randint(0,1) == 1):
            randbl = random.randint(1,255)
    return (randgr, randrd, randbl)

# Function to simulate a flame effect on built in NeoPixel (R,G,B)
def flame(pos, clr, sft):
    # pos = position, sft = shift
    if (pos + sft) > 255:
        pos = (pos + sft) - 256
    else:
        pos = (pos + sft)
    #
    # RETURN VALUES
    if pos < 32:
        # OFF
        rval = 0
    elif (pos > 31) and (pos < 64):
        # Low-High
        rval = int((pos*8) - 249)
    elif (pos > 63) and (pos < 96):
        # High-Low
        rval = int(767 - (pos*8))
    elif (pos > 95) and (pos < 128):
        # OFF
        rval = 0
    elif (pos > 127) and (pos < 160):
        # Low-High
        rval = int((pos*8) - 1017)
    elif (pos > 159) and (pos < 192):
        # High-Low
        rval = int(1535 - (pos*8))
    elif (pos > 191) and (pos < 224):
        # OFF
        rval = 0
    elif (pos > 223):
        # OFF
        rval = 0
    #
    # RETURN COLOR
    if (clr == 0):
        # Red
        return (rval, 0, 0)
    elif (clr == 1):
        # Red & Green
        return (rval, rval, 0)
    elif (clr == 2):
        # Green
        return (0, rval, 0)
    elif (clr == 3):
        # Green & Blue
        return (0, rval, rval)
    elif (clr == 4):
        # Blue
        return (0, rval, rval)
    elif (clr == 5):
        # Blue & Red
        return (rval, 0, rval)
    else:
        return (0, 0, 0)

# Function to turn off all the built in NeoPixels
def alloff():
    cpx.pixels.fill((0, 0, 0))

mode = 1
pusha = 0
pushb = 0
clr = 0
i = 0
while True:
    # NeoPixels are cpx.pixels[0-9]

    if (mode == 1):
        cpx.pixels[0] = flame(i, clr, 32)
        cpx.pixels[1] = flame(i, clr, 24)
        cpx.pixels[2] = flame(i, clr, 16)
        cpx.pixels[3] = flame(i, clr, 8)
        cpx.pixels[4] = flame(i, clr, 0)
        cpx.pixels[5] = flame(i, clr, 0)
        cpx.pixels[6] = flame(i, clr, 8)
        cpx.pixels[7] = flame(i, clr, 16)
        cpx.pixels[8] = flame(i, clr, 24)
        cpx.pixels[9] = flame(i, clr, 32)
    elif (mode == 2):
        cpx.pixels[0] = wheeln(i, 0)
        cpx.pixels[1] = wheeln(i, 24)
        cpx.pixels[2] = wheeln(i, 48)
        cpx.pixels[3] = wheeln(i, 72)
        cpx.pixels[4] = wheeln(i, 96)
        cpx.pixels[5] = wheeln(i, 120)
        cpx.pixels[6] = wheeln(i, 144)
        cpx.pixels[7] = wheeln(i, 168)
        cpx.pixels[8] = wheeln(i, 192)
        cpx.pixels[9] = wheeln(i, 216)
    elif (mode == 3):
        cpx.pixels[0] = randcolor()
        cpx.pixels[1] = randcolor()
        cpx.pixels[2] = randcolor()
        cpx.pixels[3] = randcolor()
        cpx.pixels[4] = randcolor()
        cpx.pixels[5] = randcolor()
        cpx.pixels[6] = randcolor()
        cpx.pixels[7] = randcolor()
        cpx.pixels[8] = randcolor()
        cpx.pixels[9] = randcolor()
    else:
        # Mode = 0 so turn All Off
        alloff()

    # Button A is bottom button on hat
    if cpx.button_a:
        print("Button A on Bottom Pressed! Changing mode to ALL OFF.")
        pusha = 1
    # Button B is top button on hat
    if cpx.button_b:
        print("Button B on Top Pressed! Changing mode.")
        pushb = 1

    i = (i+1) % 256
    #print (i)
    if (i == 255):
        clr = (clr+1) % 6

    if ((i == 63) | (i == 127) | (i == 191) | (i >= 255)) and (pusha == 1):
        mode = 0
        pusha = 0
        i = 0
    if ((i == 63) | (i == 127) | (i == 191) | (i >= 255)) and (pushb == 1):
        mode = (mode+1)
        pushb = 0
        i = 0
        if (mode > 3):
            mode = 1
