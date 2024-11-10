import numpy as np


class Bin:
    def __init__(self, name: str):
        self.name = name
        self.contents = np.array([])

    def add(self, item):
        self.contents = np.append(self.contents, item)

    def size(self):
        return self.contents.size

    def empty(self):
        self.contents = np.array([])
