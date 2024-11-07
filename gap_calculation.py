
class GapCalculator:
    def __init__(self, bins, num_bins: int, num_balls: int):
        self.bins = bins
        self.num_bins = num_bins
        self.num_balls = num_balls

    def gap(self):
        max_loaded_bin = max(self.bins, key=lambda b: b.size())
        gap = max_loaded_bin.size() - self.num_balls / self.num_bins
        return gap
