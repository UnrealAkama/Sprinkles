from sample_pattern import SamplePattern
import random
from patterns.common_functions import *
from itertools import cycle, islice
from random import choice


class DiamondPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.i = 1
        self.period = 200

        self.color = choice(self.colors)

        blank = (0,0,0)
        full = next(self.color)
        inner = (0,0,0)
        small_slice = [blank] * 14 + [full] * 2 + [blank] * 4 + [full] * 2 + [blank] * 14

        mid_line = [blank] + [full] + [inner] * 2 + [full] + [blank]
        medium_slice = [blank] * 6 + mid_line * 4 + [blank] * 6

        full_mid = [full] + [blank] * 4 + [full]
        full_slice = full_mid * 6

        blank_slice = [blank] * 36

        self.g = cycle([blank_slice] * 4 + [small_slice, medium_slice, full_slice, medium_slice, small_slice])

        self.results = []

        for i in range(12):
            self.results.append(next(self.g))

        self.reversed = choice([True, False])

    def tick(self):
        if self.i > self.period:
            self.i = 0
            self.results.pop(0)
            self.results.append(next(self.g))
        else:
            self.i = self.i + 1
        if self.reversed:
            return assemble_vertical_slices(self.results[::-1])
        else:
            return assemble_vertical_slices(self.results)

    def teardown(self):
        pass

class PyramidsPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.i = 1
        self.period = 200

        self.color = choice(self.colors)

        blank = (0,0,0)
        full = next(self.color)
        inner = (0,0,0)
        small_slice = [blank] * 14 + [full] * 2 + [blank] * 4 + [full] * 2 + [blank] * 14

        mid_line = [blank] + [full] + [inner] * 2 + [full] + [blank]
        medium_slice = [blank] * 6 + mid_line * 4 + [blank] * 6

        full_mid = [full] + [blank] * 4 + [full]
        full_slice = full_mid * 6

        blank_slice = [blank] * 36

        self.g = cycle([blank_slice] * 4 + [small_slice, blank_slice, medium_slice, blank_slice, full_slice])

        self.results = []

        for i in range(12):
            self.results.append(next(self.g))

        self.reversed = choice([True, False])

    def tick(self):
        if self.i > self.period:
            self.i = 0
            self.results.pop(0)
            self.results.append(next(self.g))
        else:
            self.i = self.i + 1

        if self.reversed:
            return assemble_vertical_slices(self.results[::-1])
        else:
            return assemble_vertical_slices(self.results)

    def teardown(self):
        pass

class StripsPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.i = 1
        self.period = 400
        self.perm_color = next(self.color)

    def tick(self):
        blank_slice = [self.perm_color] * 36
        full_slice = [(0, 0, 0)] * 36

        results = assemble_vertical_slices([blank_slice, full_slice] * 6)
        results_off = assemble_vertical_slices([full_slice, blank_slice] * 6)

        self.i = (self.i + 1) % self.period

        if self.i < (self.period/2):
            return results
        else:
            return results_off

    def teardown(self):
        pass

class RainbowStripsPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.i = 1
        self.period = 30

        self.color_space = 1 

        self.current = []
        self.next = []

        for i in range(20):
            self.next = self.next + [next(self.color)] * self.color_space
        while len(self.current) < 12:
            self.current.append(self.next.pop())

    def tick(self):
        results = []
        for color in self.current:
           results.append([color] * 36)

        self.i = self.i + 1
        if self.i > self.period:
            self.current.pop(0)
            self.current.append(self.next.pop())
            if len(self.next) == 0:
                self.next = self.next + [next(self.color)] * self.color_space
            self.i = 0

        return assemble_vertical_slices(results)

    def teardown(self):
        pass
