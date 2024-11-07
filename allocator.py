import random

from models import Ball, AllocationStrategy


class Allocator:
    def __init__(self, bins, num_balls, d):
        self.bins = bins
        self.num_balls = num_balls
        self.d = d

    def run(self, allocation_strategy, **kwargs):
        if allocation_strategy == AllocationStrategy.STANDARD:
            for _ in range(self.num_balls):
                self.allocate_standard(**kwargs)
        elif allocation_strategy == AllocationStrategy.D_CHOICE:
            for _ in range(self.num_balls):
                self.allocate_emptiest()
        elif allocation_strategy == AllocationStrategy.BETA_CHOICE:
            beta = kwargs.get("beta", 0.5)
            for _ in range(self.num_balls):
                self.allocate_beta_choice(beta)

    def sample_bins(self, d=None, **kwargs):
        if d is None:
            d = self.d
        return random.choices(self.bins, k=d)

    def allocate_standard(self, d=None, **kwargs):
        random.choice(self.sample_bins()).add(Ball())

    def allocate_emptiest(self, **kwargs):
        sampled_bins = self.sample_bins()
        min_size = min(sampled_bins, key=lambda b: b.size())
        emptiest_bins = [b for b in sampled_bins if b.size() == min_size.size()]
        random.choice(emptiest_bins).add(Ball())

    def allocate_beta_choice(self, beta):
        if not 0 <= beta <= 1:
            raise ValueError("Beta must be between 0 and 1")
        allocation_choice = random.choices(
            [{"f": self.allocate_standard, "d": 1}, {"f": self.allocate_emptiest, "d": 2}],
            weights=[beta, 1-beta],
        )
        allocation_choice[0]["f"](**allocation_choice[0])
