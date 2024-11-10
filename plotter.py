import matplotlib.pyplot as plt

from collections import Counter


class BinsPlotter:
    def __init__(self, bins):
        self.bins = bins
        self.bin_sizes = [b.size() for b in self.bins]

    def create_plot(self, y_value=None, title="Number of Balls in Each Bin"):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(self.bins)), self.bin_sizes, color='skyblue')
        plt.xlabel("Bins")
        plt.ylabel("Number of Balls")
        plt.title(title)
        plt.xticks(rotation=90)
        plt.tight_layout()

        if y_value is not None:
            plt.axhline(y=y_value, color='r', linestyle='-')

    @staticmethod
    def show_plot():
        plt.show()


class GapPlotter:

    def __init__(self, gaps):
        self.gaps = gaps
        self.fig, self.ax = plt.subplots()

    def plot_results(self, title="Gap distribution"):
        counter = Counter(self.gaps)
        counts = list(counter.values())
        x = list(counter.keys())

        self.ax.bar(
            x,
            counts,
            label="Bins Gap Results",
        )
        self.ax.set_title(title)
        self.ax.set_xlabel("Gap")
        self.ax.set_ylabel("Observations")
        self.ax.legend()

    @staticmethod
    def show_plot():
        plt.show()


class MeanGapPlotter:

    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel("Number of Balls")
        self.ax.set_ylabel("Mean Gap")

    def add_results(self, num_balls, mean_gaps, label="Mean Gap", color="r"):
        self.ax.plot(num_balls, mean_gaps, label=label, color=color)

    def show_plot(self, title="Mean Gap vs Number of Balls"):
        self.ax.set_title(title)
        self.ax.legend()
        plt.show()
