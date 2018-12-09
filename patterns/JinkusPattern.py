from sample_pattern import SamplePattern
import operator
import random

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

def cube(pointA, pointB):
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

def add_pts(pattern, points, color):
    # Add 'points' of 'color' to the pattern (6x6x12 input)
    for i in points:
        flat_index = get_flat_index(*i)
        pattern[flat_index] = color

    return pattern

def mask(pattern, mask):
    # Remove all 'mask' points from 'pattern'
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            for k in range(SIZE[2]):
                if (i,j,k) not in mask:
                    flat_index = get_flat_index(*(i,j,k))
                    pattern[flat_index] = (0,0,0)

    return pattern

def christmas_fire_pattern():
    pattern = []
    for i in range(36):
        intensity = random.random()
        pattern += gen_random_string(intensity*.15+.5)
    return pattern


def gen_random_string(intensity):
    n1 = random.randint(2,7)
    n2 = random.randint(4,12-n1)
    string = (
        [(0,0,0) for i in range(n1)] +
        [(0,intensity*255,0)]*(n2) + 
        [(intensity*255, intensity*40, 0)] * (12-n1-n2)
        )

    # print(len(string), n, "\n")
    return string


class JinkusPattern(SamplePattern):

    def setup(self, size=SIZE):
        super().setup()
        self.i = 0
        self.counter = 0
        self.period = 400
        self.last_pattern = [(0,0,0)] * self.max_elements

    def tick(self):
        if (self.i % self.period) == 0:
            # Blank out pattern
            pattern = results = [(0,0,0)] * self.max_elements

            # Add christmas fire pattern
            cfp = christmas_fire_pattern()
            pattern = cfp

            # Create tree pattern
            tree_pts = cube((2,2,2), (3,3,3)) + cube((1,1,4), (4,4,7)) + cube((0,0,8), (5,5,11))
            
            # Apply tree pattern as mask
            pattern = mask(pattern, tree_pts)

            # Add star pattern
            pattern = add_pts(pattern, cube((2,2,1), (3,3,1)), (255,255,0))

            self.counter+=1
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
