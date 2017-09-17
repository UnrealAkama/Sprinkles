from sample_pattern import SamplePattern
import random

class WavePattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        self.pixels = [(128,128,128)] * 84

        self.i = 0

    def tick(self):
        results = []

        for i in self.pixels:
            r = i[0] + random.randint(-1, 1)
            g = i[1] + random.randint(-1, 1)
            b = i[2] + random.randint(-1, 1)
            results.append((r,g,b))

        self.pixels = results

        return results

    def teardown(self):
        pass
