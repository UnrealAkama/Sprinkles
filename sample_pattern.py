from abc import ABC, abstractmethod
from itertools import cycle
from random import choice
from colorsys import hsv_to_rgb

hsv_output = cycle(map(lambda x : [x * 255.0 for x in hsv_to_rgb(x * 0.02, 0.5, 1.0)], range(100)))

class SamplePattern(ABC):

    # size is a 3 element that is the max size of the array.
    def setup(self, size=(6,6,12), colors=(255,255,255)):
        self.colors = [hsv_output]
        self.color = hsv_output
        self.max_elements = size[0] * size[1] * size[2]

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def teardown(self):
        pass
