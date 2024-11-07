import matplotlib.pyplot as plt


class BinsPlotter:
    def __init__(self, bins):
        self.bins = bins
        self.bin_sizes = [b.size() for b in self.bins]

    def create_plot(self, y_value=None):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(self.bins)), self.bin_sizes)
        plt.xlabel('Bins')
        plt.ylabel('Number of Balls')
        plt.title('Number of Balls in Each Bin')
        plt.xticks(rotation=90)
        plt.tight_layout()

        if y_value is not None:
            plt.axhline(y=y_value, color='g', linestyle='--')

    @staticmethod
    def show_plot():
        plt.show()
