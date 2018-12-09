from sample_pattern import SamplePattern
import operator
import random
from abc import ABC, abstractmethod

SIZE = (6,6,12)

def get_flat_index(x, y, z):
    # Remap from hardware to standard XYZ coordinates
    # After remapping:
    #   X is left-to-right
    #   Y is front-to-back
    #   Z is up-to-down

    x_mapped = z
    y_mapped = y
    z_mapped = x

    if  (0<=x and x<SIZE[0]) and (0<=y and y<SIZE[1]) and (0<=z and z<SIZE[2]):
        return x_mapped + (SIZE[2])*y_mapped + (SIZE[1]*SIZE[2])*z_mapped
    else:
        return 0

def tuplemanip(op, t_a, t_b=None):
    # Manipulate tuples with 'op' operation
    # e.g., tuplemanip(operator.add, (1,2,3), (4,5,6))
    # e.g., tuplemanip(sign, (1,2,3))
    if t_b != None:
        return tuple(map(op, t_a, t_b))
    else:
        return tuple(map(op, t_a))

def sign(i):
    if i == 0: return 1
    return int(i/abs(i))

def add_pts(pattern, colors, points=None):
    # Add 'points' of 'colors' to the pattern (6x6x12 input)
    
    if points:
        for i,pt in enumerate(points):
            flat_index = get_flat_index(*pt)
            pattern[flat_index] = colors[i]

        return pattern

    else:
        for i in range(len(colors)):
            pattern[i] = colors[i]

        return pattern


def del_pts(pattern, mask, mask_polarity):
    # If mask polarity is 1
    #   Remove all 'mask' exterior points from 'pattern'
    # Else
    #   Remove all 'mask' interior points from 'pattern'
    if mask_polarity:
        for i in range(SIZE[0]):
            for j in range(SIZE[1]):
                for k in range(SIZE[2]):
                    if (i,j,k) not in mask:
                        flat_index = get_flat_index(*(i,j,k))
                        pattern[flat_index] = (0,0,0)
    else:
        for i in range(SIZE[0]):
            for j in range(SIZE[1]):
                for k in range(SIZE[2]):
                    if (i,j,k) in mask:
                        flat_index = get_flat_index(*(i,j,k))
                        pattern[flat_index] = (0,0,0)

    return pattern

def gen_random_string(intensity):
    n1 = random.randint(1,4)
    n2 = random.randint(0,9-n1)
    string = (
        [(0,0,0) for i in range(n1)] +
        [(0,intensity*255,0)]*(n2) + 
        [(intensity*255, intensity*40, 0)] * (12-n1-n2)
        )

    # print(len(string), n, "\n")
    return string

class LightSpace():
    def __init__(self, light_objects=[], mask_objects=[]):
        self.light_objects=light_objects
        self.mask_objects=mask_objects

    def iter(self):
        # Start with blank pattern
        pattern = results = [(0,0,0)] * 6*6*12

        for lo in self.light_objects:
            lo_iteration = lo.iter()
            pattern = add_pts(pattern, lo_iteration['colormap'], lo_iteration['pixelmap'])

        # Add all mask points together
        mask_pts = []
        for mo in self.mask_objects:
            mo_iteration = mo.iter()
            mask_pts += mo_iteration['pixelmap']

        print(mask_pts)

        # Remove mask points
        pattern = del_pts(pattern, mask_pts, True)

        return pattern

class LightObject(ABC):
    def __init__(self, period=1, origin=(0,0,0)):
        self.period = period
        self.origin = origin

    @abstractmethod
    def iter(self):
        # Return colormap
        # Return pixelmap (optional)
        pass

class ChristmasFirePattern(LightObject):
    def __init__(self):
        super().__init__()

    def iter(self):
        pattern = []
        for i in range(36):
            intensity = random.random()
            pattern += gen_random_string(intensity*.15+.5)
        return {
            'pixelmap': None,
            'colormap': pattern
        }

class Cube(LightObject):
    def __init__(self, pointA, pointB, color):
        super().__init__()
        self.pixelmap = Cube.gen_pts(pointA, pointB)
        self.colormap = [color] * len(self.pixelmap)

    def iter(self):
        return {'pixelmap':self.pixelmap, 'colormap':self.colormap}

    @staticmethod
    def gen_pts(pointA, pointB):
        # Return a list of points that fall within the volume of the cube
        # Computation is inclusive of endpoints
        points = []

        deltas = tuplemanip(operator.sub, pointA, pointB)
        delta_signs = tuplemanip(sign, deltas)

        for i in range(0, deltas[0]+delta_signs[0], delta_signs[0]):
            for j in range(0, deltas[1]+delta_signs[1], delta_signs[1]):
                for k in range(0, deltas[2]+delta_signs[2], delta_signs[2]):
                    points.append(tuplemanip(operator.sub, pointA, (i,j,k)))

        return points


star = Cube((2,2,1), (3,3,1), (180,180,0))
tree_top = Cube((2,2,2), (3,3,3), (120,0,0))
tree_mid = Cube((1,1,4), (4,4,7), (120,0,0))
tree_bot = Cube((0,0,8), (5,5,11), (120,0,0))
cfp = ChristmasFirePattern()
lightspace = LightSpace([cfp, star], [tree_bot, tree_mid, tree_top, star])

class JinkusPattern(SamplePattern):

    def setup(self, size=SIZE):
        super().setup()
        self.i = 0
        self.counter = 0
        self.period = 400
        self.last_pattern = [(0,0,0)] * self.max_elements

    def tick(self):
        if (self.i % self.period) == 0:
            # # Add christmas fire pattern
            # cfp = christmas_fire_pattern()
            # pattern = cfp

            pattern = lightspace.iter()

            self.counter += 1
            self.last_pattern = pattern
        else:
            pattern = self.last_pattern

        self.i += 1
        return pattern

    def teardown(self):
        pass

    def gen_pattern_red(self, intensity):
        string = ([(0, intensity % 170,0)]*10 + [(0,0,0) for i in range(2)])

        plane = string*6

        cube = plane*6

        return cube

    def gen_pattern_green(self, intensity):
        string = ([(0,0,0) for i in range(2)] + [(intensity % 170, 0, 0)]*10)

        plane = string*6

        cube = plane*6

        return cube
