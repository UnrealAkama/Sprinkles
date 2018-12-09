# input must be an array of same sized slices
import random
from colorsys import hsv_to_rgb

def assemble_vertical_slices(slices):
    result = []
    for i in range(len(slices[0])):
        for a_slice in slices:
            result.append(a_slice[i])

    return result

def calculate(x, y, z):
    return 1*x + 12*y + 72*z

def random_color():
    c = hsv_to_rgb(random.random(), 0.5, 1.0)
    return (int(255*c[0]), int(255*c[1]), int(255*c[2]))