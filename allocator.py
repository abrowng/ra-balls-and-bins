import random

import numpy as np

from models import AllocationStrategy


class Allocator:
    def __init__(self, bins, num_balls, d):
        self.bins = bins
        self.num_balls = num_balls
        self.d = d
        self.batch_initial_state = []
        self.batch_outputs = []

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
        elif allocation_strategy == AllocationStrategy.B_BATCHED:
            b = kwargs.get("batch_size", 1)
            for i, start in enumerate(range(0, self.num_balls, b)):
                initial_bins_state = [_b.size() for _b in self.bins]
                end = min(start + b, self.num_balls)
                for _ in range(start, end):
                    self.allocate_b_batched(initial_bins_state, **kwargs)

        elif allocation_strategy == AllocationStrategy.K_MEDIAN:
            k = kwargs.get("k", 1)
            for _ in range(self.num_balls):
                self.allocate_k_median(k=k)

    def sample_bins(self, d=None, **kwargs):
        if d is None:
            d = self.d
        return random.choices(self.bins, k=d)

    def sample_bins_indices(self, d=None, **kwargs):
        if d is None:
            d = self.d
        return [random.randint(0, len(self.bins)-1) for _ in range(d)]

    def allocate_standard(self, d=None, **kwargs):
        random.choice(self.sample_bins()).add(1)

    def allocate_emptiest(self, **kwargs):
        sampled_bins = self.sample_bins()
        min_size = min(sampled_bins, key=lambda b: b.size())
        emptiest_bins = [b for b in sampled_bins if b.size() == min_size.size()]
        random.choice(emptiest_bins).add(1)

    def allocate_b_batched(self, initial_state, d=None, beta=1, **kwargs):
        if d is None:
            d = self.d
        if not 0 <= beta <= 1:
            raise ValueError("Beta must be between 0 and 1")
        sample_size = random.choices([1, d], weights=[beta, 1-beta])[0]
        sampled_bins_indices = self.sample_bins_indices(d=sample_size)
        min_size_index = min(sampled_bins_indices, key=lambda i: initial_state[i])
        emptiest_bins_indices = [i for i in sampled_bins_indices if initial_state[i] == initial_state[min_size_index]]
        emptiest_bins = [self.bins[i] for i in emptiest_bins_indices]
        bin = random.choice(emptiest_bins)
        bin.add(1)

    def allocate_beta_choice(self, beta):
        if not 0 <= beta <= 1:
            raise ValueError("Beta must be between 0 and 1")
        allocation_choice = random.choices(
            [{"f": self.allocate_standard, "d": 1}, {"f": self.allocate_emptiest, "d": 2}],
            weights=[beta, 1-beta],
        )
        allocation_choice[0]["f"](**allocation_choice[0])

    def k_partition(self, bins, sampled_bins, k):
        if k == 0:
            return sampled_bins

        bin_sizes = np.array([b.size() for b in bins])
        median_size = np.median(bin_sizes)

        smaller_or_equal_bins = []
        larger_bins = []
        new_sampled_bins = []
        for bin in sampled_bins:
            if bin.size() <= median_size:
                smaller_or_equal_bins.append(bin)
                new_sampled_bins.append(bin)
            else:
                larger_bins.append(bin)

        if len(smaller_or_equal_bins) == 1:
            return smaller_or_equal_bins
        elif len(larger_bins) == 0 and len(smaller_or_equal_bins) > 1:
            return self.k_partition([b for b in self.bins if b.size() <= median_size], smaller_or_equal_bins, k - 1)
        elif len(smaller_or_equal_bins) == 0 and len(larger_bins) > 1:
            return self.k_partition([b for b in self.bins if b.size() > median_size], larger_bins, k - 1)

    def allocate_k_median(self, d=None, k=1, **kwargs):
        if d is None:
            d = self.d
        bins_to_choose_from = self.k_partition(self.bins, self.sample_bins(d=d), k)
        random.choice(bins_to_choose_from).add(1)
