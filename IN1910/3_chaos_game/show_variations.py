import numpy as np
import matplotlib.pyplot as plt
from os import path
from os import makedirs
from variations import Variations


class ShowVariations():
    """
    Class to illustrate all the variations implemented in the
    Variations class
    """

    def setup_grid_values(self):
        """
        Sets up the grid values
        """
        N = 60
        grid_values = np.linspace(-1, 1, N, dtype=np.float64)
        self.x_values = np.ones(N*N, dtype=np.float64)
        self.y_values = np.ones(N*N, dtype=np.float64)
        for i in range(N):
            index = i*N
            self.x_values[index:index+N] *= grid_values[i]
            self.y_values[index:index+N] *= grid_values

        self.variations = Variations(self.x_values, self.y_values)

    def setup_grid_lines(self):
        """
        Sets up the grid lines
        """
        plt.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], color="grey")
        plt.plot([-1, 1], [0, 0], color="grey")
        plt.plot([0, 0], [-1, 1], color="grey")

    def plot_variation(self, method):
        """
        Plots the given variation
        """
        self.variations.call_method_str(method)
        self.variations.plot(fig = False, force_limits = True)
        self.setup_grid_lines()

    def plot_all_1fig(self):
        """
        Plots all implemented functions in one figure
        """
        self.setup_grid_values()
        n = len(self.variations.implemented_variations)
        if (path.isdir("figures") == False):
            makedirs("figures")

        plt.figure(figsize=(17,11))
        for i in range(n):
            plt.subplot(5, 3, i+1)
            self.plot_variation(self.variations.implemented_variations[i])
            plt.title(self.variations.implemented_variations[i])

        plt.tight_layout()
        plt.savefig("figures/show_all_variations.png", dpi = 400)


if __name__=="__main__":
    S = ShowVariations()
    S.plot_all_1fig()
