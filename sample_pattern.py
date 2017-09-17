from abc import ABC, abstractmethod

class SamplePattern(ABC):

    @abstractmethod
    # size is a 3 element that is the max size of the array.
    def setup(self, size=(6,6,12)):
        pass

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def teardown(self):
        pass
