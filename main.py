import numpy as np

from matplotlib import pyplot as plt

from allocator import Allocator
from gap_calculation import GapCalculator
from plotter import BinsPlotter, GapPlotter, MeanGapPlotter

from models import *

STD_TRIALS = False

PLOT_SAMPLE = True

TRIALS = [
    Trial(allocation_strat=AllocationStrategy.K_MEDIAN, balls=1000, bins=100, choices=2, repetitions=100, k_median=2),
    Trial(allocation_strat=AllocationStrategy.K_MEDIAN, balls=5000, bins=100, choices=2, repetitions=100, k_median=2),
    Trial(allocation_strat=AllocationStrategy.K_MEDIAN, balls=10000, bins=100, choices=2, repetitions=100, k_median=2),
    # Trial(allocation_strat=AllocationStrategy.B_BATCHED, balls=1000, bins=100, choices=2, repetitions=100, batch_size=2000, beta=0.5),
    # Trial(allocation_strat=AllocationStrategy.B_BATCHED, balls=6000, bins=100, choices=10, repetitions=100, batch_size=2000),
    # Trial(allocation_strat=AllocationStrategy.B_BATCHED, balls=10000, bins=100, choices=2, repetitions=100, batch_size=2000),
]


def run_std_trials():
    for i, trial in enumerate(TRIALS):

        t_repetitions = trial.repetitions
        if t_repetitions is None:
            t_repetitions = 1

        all_bins = np.array([])
        gaps = np.array([])
        for j in range(t_repetitions):
            bins = [Bin(f"Bin {i + 1}") for i in range(trial.bins)]
            allocator = Allocator(bins, trial.balls, trial.choices)

            allocator.run(
                allocation_strategy=trial.allocation_strat,
                d=trial.choices,
                beta=trial.beta,
                batch_size=trial.batch_size,
                k=trial.k_median,
            )

            if j == 0 and PLOT_SAMPLE:
                if trial.allocation_strat == AllocationStrategy.B_BATCHED:
                    for batch in allocator.batch_initial_state:
                        plotter = BinsPlotter(batch)
                        plotter.create_plot(y_value=trial.balls / trial.bins,
                                            title="Initial State before batch allocation")
                        plotter.show_plot()
                    for batch in allocator.batch_outputs:
                        plotter = BinsPlotter(batch)
                        plotter.create_plot(y_value=trial.balls / trial.bins,
                                            title="Final State after batch allocation")
                        plotter.show_plot()
                else:
                    plotter = BinsPlotter(bins)
                    plotter.create_plot(y_value=trial.balls / trial.bins)
                    plotter.show_plot()

            balls_sum = sum([b.size() for b in bins])
            if balls_sum != trial.balls:
                raise ValueError(f"Total number of balls is not equal to the number of balls allocated. "
                                 f"Expected: {trial.balls}, Actual: {balls_sum}")
            calc = GapCalculator(bins, trial.bins, trial.balls)
            gaps = np.append(gaps, calc.gap())
            all_bins = np.append(all_bins, [b.size() for b in bins])

        gaps_plotter = GapPlotter(gaps)
        gaps_plotter.plot_results(f"Gap distribution for {trial.allocation_strat.value} allocation (n={trial.balls}, d={trial.choices}, k={trial.k_median})")
        gaps_plotter.show_plot()
        print(
            f"Test {i + 1} (Allocation: {trial.allocation_strat.value}, n: {trial.balls}, "
            f"m: {trial.bins}, d: {trial.choices}, T: {t_repetitions}, b: {trial.batch_size}): "
        )
        print(
            f"\tMean Gap: {np.mean(gaps)}\n"
            f"\tStandard Deviation: {np.std(gaps)}\n"
            f"\tVariance: {np.var(gaps)}\n"
        )


def run_batched_trials(strat=AllocationStrategy.B_BATCHED, bins=100, repetitions=100, d=1, beta=1, k=1):
    increasing_batch_size = [
        1*bins,
        #2*bins,
        #5*bins,
        #10*bins,
        #20*bins,
        #50*bins,
        #bins*bins,
    ]

    increasing_d = [
        2, 3, 4
    ]

    for d in increasing_d:
        increasing_n = [
            1 * bins,
            2 * bins,
            5 * bins,
            7 * bins,
            10 * bins,
            15 * bins,
            20 * bins,
            30 * bins,
            40 * bins,
            45 * bins,
            50 * bins,
            55 * bins,
            60 * bins,
            65 * bins,
            75 * bins,
            85 * bins,
            bins * bins,
        ]

        batch_size_mean_gaps = np.array([])

        for n in increasing_n:
            gaps = np.array([])

            for j in range(repetitions):
                trial_bins = [Bin(f"Bin {i + 1}") for i in range(bins)]
                allocator = Allocator(trial_bins, n, d)

                allocator.run(
                    allocation_strategy=strat,
                    d=d,
                    beta=beta,
                    #batch_size=batch_size,
                    k=k,
                )

                calc = GapCalculator(trial_bins, bins, n)
                gaps = np.append(gaps, calc.gap())
            batch_size_mean_gaps = np.append(batch_size_mean_gaps, np.mean(gaps))

        yield batch_size_mean_gaps, increasing_n, d


def get_single_hue_colors(colormap_name, num_colors):
    colormap = plt.get_cmap(colormap_name)
    return [colormap(i / num_colors) for i in range(num_colors)]


if __name__ == "__main__":

    if STD_TRIALS:
        run_std_trials()
    else:
        d_values = [2, 3, 4, 5]
        beta_values = [0.8]
        k_medians = [1]

        plotter = MeanGapPlotter()
        main_colors = ['Greens', 'Reds', 'Purples', 'Blues', 'Grays', 'Oranges']

        ### Uncomment the following to run the batched trials for different values of d, beta, and batch_size
        # for i, beta in enumerate(beta_values):
        #     plot_colors = get_single_hue_colors(main_colors[-i], 9)
        #     for results in run_batched_trials(beta=beta, d=2):
        #         plotter.add_results(results[1], results[0], label=f"Beta: {beta}, Batch Size: {results[2]}",
        #                             color=plot_colors.pop())

        ### Uncomment the following to run the d-choice trials for different values of d
        # for i, d in enumerate(d_values):
        #     plot_colors = get_single_hue_colors(main_colors[i], 9)
        #     for results in run_batched_trials(d=d, strat=AllocationStrategy.D_CHOICE):
        #         plotter.add_results(results[1], results[0], label=f"d={d}",
        #                             color=plot_colors.pop())

        ### Uncomment the following to run the k-means trials for different values of k
        for i, k in enumerate(k_medians):
            plot_colors = get_single_hue_colors(main_colors[i], 9)
            for results in run_batched_trials(strat=AllocationStrategy.K_MEDIAN, k=k):
                plotter.add_results(results[1], results[0], label=f"d={results[2]}, k={k}",
                                    color=plot_colors.pop())
        plotter.show_plot(title=f"Mean Gap vs Number of Balls")
