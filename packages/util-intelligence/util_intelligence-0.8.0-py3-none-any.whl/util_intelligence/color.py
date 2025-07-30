import random


class ColorBGR:
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    LIGHTGRAY = 191, 191, 191
    GREEN = 0, 127, 0
    MAGENTA = 255, 0, 255
    YELLOW = 0, 255, 255
    LIME = 0, 255, 0
    AQUA = 255, 255, 0
    BLUE = 255, 0, 0
    RED = 0, 0, 255

    @staticmethod
    def random_color(start, end, opacity=None):
        red = random.randint(start, end)
        green = random.randint(start, end)
        blue = random.randint(start, end)
        if opacity is None:
            return (red, green, blue)
        return (red, green, blue, opacity)


class ColorHSV:
    BLACK = [[180, 255, 30], [0, 0, 0]]
    WHITE = [[180, 18, 255], [0, 0, 231]]
    RED1 = [[180, 255, 255], [159, 50, 70]]
    RED2 = [[9, 255, 255], [0, 50, 70]]
    GREEN = [[89, 255, 255], [36, 50, 70]]
    BLUE = [[128, 255, 255], [90, 50, 70]]
    YELLOW = [[35, 255, 255], [25, 50, 70]]
    PURPLE = [[158, 255, 255], [129, 50, 70]]
    ORANGE = [[24, 255, 255], [10, 50, 70]]
    GRAY = [[180, 18, 230], [0, 0, 40]]


def scope_color(c: int):
    return min(max([0, c]), 255)
