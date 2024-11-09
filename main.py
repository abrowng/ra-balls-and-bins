from allocator import Allocator
from gap_calculation import GapCalculator
from plotter import BinsPlotter, GapPlotter

from models import *

PLOT_SAMPLE = False

TRIALS = [
    Trial(allocation_strat=AllocationStrategy.B_BATCHED, balls=500, bins=100, choices=1, repetitions=10, batch_size=100),
]

if __name__ == "__main__":

    for i, trial in enumerate(TRIALS):

        t_repetitions = trial.repetitions
        if t_repetitions is None:
            t_repetitions = 1

        all_bins = np.array([])
        gaps = np.array([])
        for j in range(t_repetitions):
            bins = [Bin(f"Bin {i+1}") for i in range(trial.bins)]
            allocator = Allocator(bins, trial.balls, trial.choices)

            allocator.run(
                allocation_strategy=trial.allocation_strat,
                d=trial.choices,
                beta=trial.beta,
                batch_size=trial.batch_size,
            )

            if j == 0 and PLOT_SAMPLE:
                if trial.allocation_strat == AllocationStrategy.B_BATCHED:
                    for batch in allocator.batch_initial_state:
                        plotter = BinsPlotter(batch)
                        plotter.create_plot(y_value=trial.balls / trial.bins, title="Initial State before batch allocation")
                        plotter.show_plot()
                    for batch in allocator.batch_outputs:
                        plotter = BinsPlotter(batch)
                        plotter.create_plot(y_value=trial.balls / trial.bins, title="Final State after batch allocation")
                        plotter.show_plot()
                else:
                    plotter = BinsPlotter(bins)
                    plotter.create_plot(y_value=trial.balls / trial.bins)
                    plotter.show_plot()

            calc = GapCalculator(bins, trial.bins, trial.balls)
            gaps = np.append(gaps, calc.gap())
            all_bins = np.append(all_bins, [b.size() for b in bins])

        gaps_plotter = GapPlotter(gaps)
        gaps_plotter.plot_results()
        gaps_plotter.show_plot()
        print(
            f"Test {i+1} (Allocation: {trial.allocation_strat.value}, n: {trial.balls}, "
            f"m: {trial.bins}, d: {trial.choices}, T: {t_repetitions}: "
        )
        print(
            f"\tMean Gap: {np.mean(gaps)}\n"
            f"\tStandard Deviation: {np.std(gaps)}\n"
            f"\tVariance: {np.var(gaps)}\n"
        )


