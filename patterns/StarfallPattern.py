from sample_pattern import SamplePattern
import random
from patterns.common_functions import *
from itertools import cycle, islice
from random import choice, randint


class ColumnsPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.i = 1
        self.period = 200
        self.stars = []

        self.reversed = choice([True, False])
        self.trail = choice([2,3,4,12])

        if self.reversed:
            # this change direction
            self.offset = 11
            self.judge = 0
            self.direction = -1
        else:
            self.offset = 0
            self.judge = 11
            self.direction = 1


        self.stars.append((calculate(0, randint(0, 5), randint(0, 5)) + self.offset, next(self.color)))

    def tick(self):
        if self.i > self.period:
            self.i = 0
            # do logic here
            delete = []
            for star in range(len(self.stars)):
                pos = self.stars[star][0]
                color = self.stars[star][1]
                if pos % 12 == self.judge:
                    delete.append(star)
                else:
                    self.stars[star] = (pos + self.direction, color)

            for item in delete:
                self.stars.pop(item)
            self.stars.append((calculate(0, randint(0, 5), randint(0, 5)) + self.offset, next(self.color)))
        else:
            self.i = self.i + 1

        results = [(0,0,0)] * self.max_elements

        for star in self.stars:
            if self.reversed:
                to_change = range(star[0], star[0] + min((12 - (star[0] % 12)), self.trail), 1)
            else:
                to_change = range(star[0], star[0] - min((star[0] % 12) -1, self.trail) -2 , -1)
            for pixel in to_change:
                results[pixel] = star[1]

        return results

    def teardown(self):
        pass

class IcicleStarfallPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.i = 1
        self.period = 50
        self.stars = []

        if randint(1, 2) == 1:
            # this change direction
            self.offset = 11
            self.judge = 0
            self.direction = -1
        else:
            self.offset = 0
            self.judge = 11
            self.direction = 1


        self.stars.append((calculate(0, randint(0, 5), randint(0, 5)) + self.offset, next(self.color)))


    def tick(self):
        if self.i > self.period:
            self.i = 0
            # do logic here
            pooling = []
            delete = []
            for star in range(len(self.stars)):
                pos = self.stars[star][0]
                color = self.stars[star][1]
                if pos % 12 == self.judge:
                    pooling.append(pos)
                elif pos + self.direction in pooling:
                    pooling.append(pos)
                else:
                   self.stars[star] = (pos + self.direction, color)

            for item in delete:
                self.stars.pop(item)

            self.stars.append((calculate(0, randint(0, 5), randint(0, 5)) + self.offset, next(self.color)))
        else:
            self.i = self.i + 1

        results = [(0,0,0)] * self.max_elements

        for star in self.stars:
            results[star[0]] = star[1]

        return results

    def teardown(self):
        pass

class PoolingStarfallPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.i = 1
        self.period = 200
        self.stars = []

        if randint(1, 2) == 1:
            # this change direction
            self.offset = 11
            self.judge = 0
            self.direction = -1
        else:
            self.offset = 0
            self.judge = 11
            self.direction = 1


        self.stars.append((calculate(0, randint(0, 5), randint(0, 5)) + self.offset, next(self.color)))

    def tick(self):
        if self.i > self.period:
            self.i = 0
            # do logic here
            pooling = []
            delete = []
            for star in range(len(self.stars)):
                pos = self.stars[star][0]
                color = self.stars[star][1]
                if pos % 12 == self.judge:
                    positions = list(map(lambda x: self.stars[x][0], pooling))
                    if pos in positions:
                        # star is in pooling
                        delete.append(positions.index(pos))
                    pooling.append(star)
                else:
                    self.stars[star] = (pos + self.direction, color)

            for item in delete:
                self.stars.pop(item)

            self.stars.append((calculate(0, randint(0, 5), randint(0, 5)) + self.offset, next(self.color)))
        else:
            self.i = self.i + 1

        results = [(0,0,0)] * self.max_elements

        for star in self.stars:
            results[star[0]] = star[1]

        return results

    def teardown(self):
        pass

class StarfallPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()
        self.i = 1
        self.period = 200
        self.stars = []

        if randint(1, 2) == 1:
            # this change direction
            self.offset = 11
            self.judge = 0
            self.direction = -1
        else:
            self.offset = 0
            self.judge = 11
            self.direction = 1


        self.stars.append((calculate(0, randint(0, 5), randint(0, 5)) + self.offset, next(self.color)))

    def tick(self):
        if self.i > self.period:
            self.i = 0
            # do logic here
            delete = []
            for star in range(len(self.stars)):
                pos = self.stars[star][0]
                color = self.stars[star][1]
                if pos % 12 == self.judge:
                    delete.append(star)
                else:
                    self.stars[star] = (pos + self.direction, color)

            for item in delete:
                self.stars.pop(item)
            self.stars.append((calculate(0, randint(0, 5), randint(0, 5)) + self.offset, next(self.color)))
        else:
            self.i = self.i + 1

        results = [(0,0,0)] * self.max_elements

        for star in self.stars:
            results[star[0]] = star[1]

        return results

    def teardown(self):
        pass
