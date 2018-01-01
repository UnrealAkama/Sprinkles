from sample_pattern import SamplePattern
import random, time, math
from patterns.common_functions import calculate as coords_to_index
from patterns.common_functions import random_color

acceleration = -9.8

def render_turned_on(set):
    results = [(0,0,0) for k in range(6*6*12)]
    for color, pos in set:
        x, y, z = pos
        index = coords_to_index(z,y,x)
        results[index] = color
        
    return results

class Ball():
    
    def __init__(self, x=0, y=0):
        self.color = random_color()
        self.z = 2
        self.x = x
        self.y = y
        self.velocity = 0
        self.last = time.time()
        self.elasticity = random.uniform(0.5, 0.85)

    def tick(self):
        start = time.time()
        delta = start - self.last
        self.last = start
        
        self.z = min(2, max(0, 0.5*(delta**2)*acceleration + self.velocity*delta + self.z))
        self.velocity += acceleration*delta
        
        if (self.z == 0):
            self.z += 0.0001
            self.velocity = self.elasticity * abs(self.velocity)
    
    def render(self):
        z = 11 - math.floor(self.z * 6)
        return self.color, (self.x, self.y, z)
        

class BouncePattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.pixels = []

        self.balls = []
        for x in range(size[0]):
            for y in range(size[1]):
                self.balls.append(Ball(x, y))

    def tick(self):
        results = []

        for ball in self.balls:
            ball.tick()
            results.append(ball.render())

        return render_turned_on(results)

    def teardown(self):
        return [(0,0,0) for k in range(6*6*12)]
