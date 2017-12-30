from sample_pattern import SamplePattern
import random
from common_functions import *

class PyramidsPattern(SamplePattern):

    def setup(self, size=(6,6,12)):
        super().setup()

    def tick(self):
        blank_slice = [0] * 36
        full_slice = [1] * 36

        results = assemble_vertical_slices([blank_slice, full_slice] * 3)

        return results

    def teardown(self):
        pass
