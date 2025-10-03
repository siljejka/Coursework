import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from os import path
from os import makedirs


class ChaosGame():
    """
    A class which illustrates how complex patterns in the form of fractals
    occur from simple sets of rules.

    The class sets up an n-gon, then takes a random starting point and
    generates new points by picking a random corner and moving towards it by a
    fraction of the distance to the corner.
    """

    def __init__(self, n = 3, r = 0.5):
        """
        n: the number of corners in the n-gon
        r: the factor of the distance to the corner moved from a point each
        iteration

        The init then calls self._generate_ngon() and generates the corners.
        """
        if (n>=3):
            if isinstance(n, int):
                self.n = n
            elif n%1 == 0:
                self.n = int(n)
            else:
                raise ValueError("n has to be an integer.")
        else:
            raise ValueError("n has to be greater than 2.")

        if (0<r<1):
            self.r = r
        else:
            raise ValueError("r has to be between 0 and 1.")

        self._generate_ngon()

    def _generate_ngon(self):
        """
        Shapes the n-gon by generating n evenly distributed points on a
        circle.
        """
        self.rads = np.linspace(0, 2*np.pi, self.n+1)
        self.corners = np.zeros((self.n, 2), dtype=np.float64)
        for i in range(self.n):
            self.corners[i,:] = [np.sin(self.rads[i]), np.cos(self.rads[i])]

    def _plot_ngon(self):
        """
        Plots the corners of the n-gon.
        """
        plt.figure(figsize=(9,7))
        plt.axis("equal")
        plt.plot(self.corners[:,0], self.corners[:,1], "k--", lw=0.5)
        plt.plot([self.corners[-1][0], self.corners[0][0]],
                 [self.corners[-1][1], self.corners[0][1]], "k--", lw=0.5)
        plt.scatter(self.corners[:,0], self.corners[:,1], c="k")
        plt.show()
        plt.clf()

    def _starting_point(self):
        """
        Creates n random values, then scales them so their sum is 1. The method
        then picks a starting point by applying these values as factors of the
        corners.
        """
        weight = np.random.random(self.n)
        weight = weight/np.sum(weight)

        self.start = np.zeros(2)
        for i in range(self.n):
            self.start += self.corners[i,:]*weight[i]

    def iterate(self, steps = 1000, discard = 5, use_fast = True):
        """
        Method that first iterates and discards set of points to prevent values
        not consistent with the fractal, then iterates a number of steps and
        saves the points internally.

        The method draws steps random numbers before it starts iterating,
        this means it only calls np.random.randint() once instead of steps
        times.

        The method has an option for either iterating within the method itself
        or iterating using a faster function compiled using Numba.

        steps: how many steps to iterate for
        discard: how many steps to discard
        use_fast: boolean which decides which method to use
        """
        D_N = np.random.randint(0, self.n, discard)
        for i in range(discard):
            self.start = ((self.start * self.r) +
                         ((1-self.r) * self.corners[D_N[i],:]))

        self.points = np.zeros((steps,2), dtype=np.float64)
        self.points[0,:] = self.start

        if use_fast == True:
            self.points, self.N = iterate_fast(self.corners, steps,
                                               self.points, self.r,
                                               self.n)
        else:
            self.N = np.random.randint(0, self.n, steps)
            for i in range(1, steps):
                self.points[i,:] = ((self.points[i-1]*self.r) +
                                    (1-self.r) * self.corners[self.N[i],:])

    def plot(self, color=False, cmap="cividis_r"):
        """
        Plots the fractal, giving a choice of plotting it with or without
        colour, and in the case of colour which colour map to use.
        """
        if color == False:
            colors = "black"
        else:
            colors = self._compute_color()

        plt.figure(figsize=(9,7))
        plt.axis("equal")
        plt.scatter(self.points[:,0], self.points[:,1], c=colors, cmap=cmap,
                    s=0.1)
        plt.tight_layout()

    def show(self, color=False, cmap="cividis_r"):
        """
        Method that runs the plot funcction and shows the figure.
        """
        self.plot(color=color, cmap=cmap)
        plt.show()

    def savepng(self, outfile, color=False, cmap="cividis_r", dpi=300,
                transparent=False):
        """
        Method that runs the plot function and saves the figure as a png.

        Takes an input of file name, dots per inch, and whether the file should
        have a transparent background.
        """
        self.plot(color=color, cmap=cmap)

        if ".png" in outfile:
            filename = outfile
            plt.savefig(filename, dpi=dpi, transparent=transparent)
        elif "." in outfile:
            raise Exception("File must be .png format")
        else:
            filename = "%s.png" %(outfile)
            plt.savefig(filename, dpi=dpi, transparent=transparent)
            plt.close()

    def _compute_color(self):
        """
        Method which generates and returns a list of gradient colour values.
        """
        steps = len(self.N)
        c_array = np.zeros(steps)
        c_array[0] = self.N[0]

        for i in range(1,steps):
            c_array[i] = (c_array[i-1] + self.N[i]) / 2

        return c_array

@jit(cache=True, nopython=True)
def iterate_fast(corners, steps, points, r, n):
    """
    Function that increases the speed that the class iterates through points.

    corners: array containing the coordinates of the corners
    steps: how many steps to iterate for
    points: array should be of the shape (steps, 2), with (0,:) being the
            starting point
    r: the value of r to use for the iteration
    n: the number of corners to use
    """
    N = np.random.randint(0, n, steps)
    for i in range(1, steps):
        points[i] = (points[i-1]*r) + ((1-r) * corners[N[i],:])
    return points, N

def make_figures(n_vals = [3,4,5,5,6],
                 r_vals = [1./2, 1./3, 1./3, 3./8, 1./3],
                 steps = 1e6, filename = "chaos"):
    """
    Function which creates n figures with n_vals corners, with points moving a
    factor r of the distance to a corner from the same index r_vals.
    """
    msg = "n_vals and r_vals must have an equal amount of values."
    assert len(n_vals) == len(r_vals), msg

    for i in range(len(n_vals)):
        CG = ChaosGame(n=n_vals[i], r=r_vals[i])
        CG._starting_point()
        CG.iterate(steps = int(steps))
        if (path.isdir("figures") == False):
            makedirs("figures")
        CG.savepng("figures/%s%d"%(filename,i+1), dpi=1200, color=True)


if __name__=="__main__":
    make_figures()
