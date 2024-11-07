from allocator import Allocator
from gap_calculation import GapCalculator
from plotter import BinsPlotter

from models import *

TRIALS = [
    Trial(allocation_strat=AllocationStrategy.STANDARD, balls=100, bins=100, d=1),
    Trial(allocation_strat=AllocationStrategy.STANDARD, balls=500, bins=100, d=1),
    Trial(allocation_strat=AllocationStrategy.STANDARD, balls=1000, bins=100, d=1),
    Trial(allocation_strat=AllocationStrategy.STANDARD, balls=10000, bins=100, d=1),
]

if __name__ == "__main__":

    for i, trial in enumerate(TRIALS):
        bins = [Bin(f"Bin {i+1}") for i in range(trial.bins)]
        allocator = Allocator(bins, trial.balls, trial.d)

        allocator.run(allocation_strategy=trial.allocation_strat, d=trial.d)

        plotter = BinsPlotter(bins)
        plotter.create_plot(y_value=trial.balls / trial.bins)
        plotter.show_plot()

        calc = GapCalculator(bins, trial.bins, trial.balls)
        print(f"Gap for test {i+1} (Allocation: {trial.allocation_strat}, Balls: {trial.balls}, Bins: {trial.bins}): {calc.gap()}")

