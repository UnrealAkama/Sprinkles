from sample_pattern import SamplePattern
import random

class JinkusPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.i = 0
        self.period=200
        self.last_pattern = [(0,0,0)] * self.max_elements

    def tick(self):
        # if (self.i % self.period) == 0:
        #     pattern = self.gen_pattern_green(self.i/8.0)
        #     self.last_pattern = pattern
        #     return pattern
        # else:
        #     pattern = self.gen_pattern_red(self.i/8.0)
        #     self.last_pattern = pattern
        #     return pattern
        #     return self.last_pattern

        if (self.i % self.period) == 0:
            pattern = []
            for i in range(36):
                intensity = random.random()
                pattern += self.gen_random_string(intensity*.2+.5)
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

class PinkusPattern(JinkusPattern):

    def setup(self, size=(6,6,12)):
        super().setup()

        self.change = -1

    def tick(self):
        return super().tick()

    def teardown(self):
        super().teardown()
