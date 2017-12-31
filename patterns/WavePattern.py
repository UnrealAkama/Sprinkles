from sample_pattern import SamplePattern
import random
from colorsys import hsv_to_rgb
from itertools import cycle

class WavePattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.pixels = list(map(lambda x : (random.randint(0, 100) * 0.02, 0.5, 0.3), range(self.max_elements)))

        self.i = 0

    def tick(self):
        results = []

        for i in self.pixels:
            r = i[0] + random.randint(-3, 3) * 0.02
            b = min(i[2] + 0.0002, 1.0)
            results.append((r,i[1],b))

        self.pixels = results

        output = list(map(lambda y : [x * 255.0 for x in hsv_to_rgb(y[0], y[1], y[2])], self.pixels))
        return output

    def teardown(self):
        pass

class ChoasWavePattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.pixels = list(map(lambda x : hsv_to_rgb(random.randint(0, 100) * 0.02, 0.3, 0.3), range(self.max_elements)))

        self.direction = 1
        self.step = 0.0006


        self.i = 0

    def tick(self):
        results = []

        for i in self.pixels:
            r = i[2] + random.randint(-1, 1) * 0.02
            if i[0] >= (1.0 - self.step):
                self.direction = -1
            if i[0] <= (self.step):
                self.direction = 1
            b = i[0] + (self.direction * self.step)
            results.append((b, i[1], r))
        self.pixels = results

        output = list(map(lambda y : [x * 255.0 for x in (y[0], y[1], y[2])], self.pixels))
        return output

    def teardown(self):
        pass

class BroadWavePattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()

        self.i = 0

        self.color = cycle(map(lambda x : (x * 0.02, 0.4, .7), range(100)))

    def tick(self):
        results = []

        if self.i % 100 == 0:
            self.tracked = next(self.color)

        for i in range(self.max_elements):
            r = self.tracked[0] + random.randint(-1, 1)
            
            results.append((r,self.tracked[1],self.tracked[2]))

        self.i = self.i + 1

        output = list(map(lambda y : [x * 255.0 for x in hsv_to_rgb(y[0], y[1], y[2])], results))
        return output

    def teardown(self):
        pass
