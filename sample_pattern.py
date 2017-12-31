from abc import ABC, abstractmethod
from itertools import cycle
from random import choice

WHITE = cycle([(255, 255, 255)])
BLUE = cycle([(0, 0, 255)])
RED = cycle([(0, 255, 0)])
GREEN = cycle([(255, 0, 0)])

SAMPLE_COLORS = [WHITE, BLUE, RED, GREEN]

class SamplePattern(ABC):

    # size is a 3 element that is the max size of the array.
    def setup(self, size=(6,6,12), colors=SAMPLE_COLORS):
        self.colors = colors
        self.color = choice(self.colors)
        self.max_elements = size[0] * size[1] * size[2]

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def teardown(self):
        pass
