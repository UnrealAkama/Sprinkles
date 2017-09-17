from sample_pattern import SamplePattern
import random

class RandomBlinkPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        self.pixels = []

        self.i = 0

    def tick(self):
        results = []

        for i in range(84):
            if i == self.i:
                choice = random.choice([(128,0,0), (0,128,0), (0,0,128)])
                results.append(choice)

            else:
                results.append((0,0,0))
        self.i = (self.i + 1) % 84

        return results

    def teardown(self):
        pass
