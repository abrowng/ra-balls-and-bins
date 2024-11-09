from allocator import Allocator
from gap_calculation import GapCalculator
from plotter import BinsPlotter, GapPlotter

from models import *

TRIALS = [
    Trial(allocation_strat=AllocationStrategy.STANDARD, balls=100, bins=100, d=1, T=100),
    Trial(allocation_strat=AllocationStrategy.STANDARD, balls=500, bins=100, d=1, T=100),
    Trial(allocation_strat=AllocationStrategy.STANDARD, balls=1000, bins=100, d=1, T=100),
    Trial(allocation_strat=AllocationStrategy.STANDARD, balls=10000, bins=100, d=1, T=100),
]

if __name__ == "__main__":

    for i, trial in enumerate(TRIALS):

        t_repetitions = trial.T
        if t_repetitions is None:
            t_repetitions = 1

        all_bins = np.array([])
        gaps = np.array([])
        for j in range(t_repetitions):
            bins = [Bin(f"Bin {i+1}") for i in range(trial.bins)]
            allocator = Allocator(bins, trial.balls, trial.d)

            allocator.run(allocation_strategy=trial.allocation_strat, d=trial.d)

            calc = GapCalculator(bins, trial.bins, trial.balls)
            gaps = np.append(gaps, calc.gap())
            all_bins = np.append(all_bins, [b.size() for b in bins])

            if j == 0:
                plotter = BinsPlotter(bins)
                plotter.create_plot(y_value=trial.balls / trial.bins)
                plotter.show_plot()

        gaps_plotter = GapPlotter(gaps)
        gaps_plotter.plot_results()
        gaps_plotter.show_plot()
        print(
            f"Mean gap for test {i+1} (Allocation: {trial.allocation_strat}, "
            f"Balls: {trial.balls}, Bins: {trial.bins}): {np.mean(gaps)}"
        )

