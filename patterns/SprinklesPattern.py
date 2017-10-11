from sample_pattern import SamplePattern
import random

class SprinklesPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        self.pixels = []

        self.i = 0

    def tick(self):
        results = []

        for i in range(512):
            if i == self.i:
                # choice = random.choice([(128,0,0), (0,128,0), (0,0,128)])
                results.append((random.randint(0,255), random.randint(0,255), random.randint(0,255)))

            else:
                results.append((0,0,0))
        self.i = (self.i + 1) % 512

        return results

    def teardown(self):
        pass
