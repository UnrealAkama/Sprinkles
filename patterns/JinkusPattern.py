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

    # print(deltas)
    # print(delta_signs)

    for i in range(0, deltas[0]+delta_signs[0], delta_signs[0]):
        for j in range(0, deltas[1]+delta_signs[1], delta_signs[1]):
            for k in range(0, deltas[2]+delta_signs[2], delta_signs[2]):
                points.append(tuplemanip(operator.sub, pointA, (i,j,k)))

    # print(points)

    return points

def add_pts(pattern, points, color):
    # Add 'points' of 'color' to the pattern (6x6x12 input)
    for i in points:
        flat_index = get_flat_index(*i)
        pattern[flat_index] = color

    return pattern

class JinkusPattern(SamplePattern):

    def setup(self, size=SIZE):
        super().setup()
        self.i = 0
        self.counter = 0
        self.period=10
        self.last_pattern = [(0,0,0)] * self.max_elements

    def tick(self):
        if (self.i % self.period) == 0:
            # pattern = []
            # for i in range(36):
            #     intensity = random.random()
            #     pattern += self.gen_random_string(intensity*.4+.2)
            # self.last_pattern = pattern


            pattern = results = [(0,0,0)] * self.max_elements
            pattern = add_pts(pattern, cube((2,2,1), (3,3,1)), (255,255,0))
            pattern = add_pts(pattern, cube((2,2,2), (3,3,3)), (200,0,0))
            pattern = add_pts(pattern, cube((1,1,4), (4,4,7)), (200,0,0))
            pattern = add_pts(pattern, cube((0,0,8), (5,5,11)), (200,0,0))
            # pattern = add_pts(pattern, cube((2,2,4), (3,3,8)), (255,0,0))
            # pattern = add_pts(pattern, cube((1,1,9), (4,4,11)), (255,0,0))

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

    def gen_random_string(self, intensity):
        n1 = random.randint(2,7)
        n2 = random.randint(4,12-n1)
        string = (
            [(0,0,0) for i in range(n1)] +
            [(0,intensity*255,0)]*(n2) + 
            [(intensity*255, intensity*220, intensity*200)] * (12-n1-n2)
            )

        # print(len(string), n, "\n")
        return string
