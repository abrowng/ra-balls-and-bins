
class Bin:
    def __init__(self, name: str):
        self.name = name
        self._size = 0

    def add(self, count):
        self._size += count

    def size(self):
        return self._size

    def __lt__(self, other):
        return self.size() < other.size()
