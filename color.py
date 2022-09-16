BLACK = (0, 0, 0)
RED = (244, 67, 54)
PINK = (234, 30, 99)
PURPLE = (156, 39, 176)
DEEP_PURPLE = (103, 58, 183)
BLUE = (33, 150, 243)
TEAL = (0, 150, 136)
L_GREEN = (139, 195, 74)
GREEN = (60, 175, 80)
ORANGE = (255, 152, 0)
DEEP_ORANGE = (255, 87, 34)
BROWN = (121, 85, 72)
WHITE = (255, 255, 255)

colour_dict = {0: BLACK, 2: RED, 4: PINK, 8: PURPLE, 16: DEEP_PURPLE, 32: BLUE, 64: TEAL, 128: L_GREEN, 256: GREEN,
               512: ORANGE, 1024: DEEP_ORANGE, 2048: BROWN, 4096: RED, 8192: PINK, 16384: PURPLE, 32768: DEEP_PURPLE}


def getColour(i):
    if i in colour_dict:
        return colour_dict[i]
    else:
        return DEEP_PURPLE
