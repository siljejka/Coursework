import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from numba import jit


class Triangle():

    """
    Class to illustrate and calculate the Chaos Game for a triangle
    """

    def __init__(self):
        """
        Sets up the corners of our equilateral triangle
        """
        self.corners = np.asarray([[0,0], [1,0], [0.5,np.sqrt(0.75)]])

    def plot_triangle(self):
        """
        Plots the triangle with corners and lines between them
        """
        plt.figure(figsize=(9,7))
        plt.scatter(self.corners[:,0], self.corners[:,1], c = "r", s = 5)
        plt.plot([self.corners[-1,0], self.corners[0,0]],
                 [self.corners[-1,1], self.corners[0,1]], "k--", lw=0.5)
        plt.plot(self.corners[:,0], self.corners[:,1], "k--", lw=0.5)
        plt.show()

    def _starting_point(self):
        """
        Draws three random values between 0 and 1, scales them so their sum is 1,
        then finds a starting point by taking a linear combination of the
        corners and using the random values as scalars for the corners.
        """
        self.start = np.zeros(2, dtype=np.float64)
        self.weights = np.random.random(3)
        self.weights = self.weights/np.sum(self.weights)
        for i in range(3):
            self.start += self.corners[i]*self.weights[i]

    def check_starting_point(self, N = 1000):
        """
        Plots the triangle with corners and lines between them, draws N
        random starting points and plots them so we can visually confirm that
        they all land within the triangle
        """
        plt.figure(figsize=(9,7))
        plt.scatter(self.corners[:,0], self.corners[:,1], c = "r", s=5)
        plt.plot([self.corners[-1,0], self.corners[0,0]],
                 [self.corners[-1,1], self.corners[0,1]], "k--", lw=0.5)
        plt.plot(self.corners[:,0], self.corners[:,1], "k--", lw=0.5)

        starting_points = np.zeros((N,2), dtype=np.float64)
        for i in range(N):
            self._starting_point()
            starting_points[i] = self.start

        plt.scatter(starting_points[:,0], starting_points[:,1], c="k", s=0.1)
        plt.show()

    def iterate(self, steps = 10000, discard = 5, use_fast = True):
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

        D_N = np.random.randint(0, 3, discard)
        for i in range(3):
            self.start = ((self.start + self.corners[D_N[i]]) * 0.5)

        self.points = np.zeros((steps,2))
        self.points[0,:] = self.start

        if use_fast == True:
            self.points, self.N = iterate_fast(self.corners, steps, self.points)
        else:
            self.N = np.random.randint(0,3,steps)
            for i in range(1, steps):
                self.points[i,:] = ((self.points[i-1]+self.corners[self.N[i]])
                                   *0.5)

    def plot(self, c = None, cmap = None):
        """
        Plots the fractal, giving a choice of plotting it with or without
        colour, and in the case of colour which colour map to use.
        """
        plt.figure(figsize=(9,7))
        plt.axis("equal")
        plt.axis("off")
        plt.scatter(self.points[:,0], self.points[:,1],
                    c=c, cmap = cmap, marker=".", s=0.1)
        plt.show()

    def plot_color(self):
        """
        Plots the fractal with a colormap that sets the color according to
        which corner the step traveled towards
        """
        cmap = ListedColormap(["red", "green", "blue"])
        self.plot(c=self.N, cmap=cmap)

    def plot_rbg(self, use_fast = True):
        """
        Plots the fractal with a colormap that sets the color as an RGB value
        thats a combination of the point the step is travelling towards and
        the last step it travelled towards
        """
        self.r = np.asarray([[1,0,0], [0,1,0], [0,0,1]])
        self.C = np.zeros((len(self.N), 3), dtype=np.float64)
        for i in range(3):
            self.C[0,i] = self.weights[i]

        if use_fast == True:
            self.C = iterate_rgb_fast(self.C, self.N, self.r)
        else:
            self.iterate_rgb()

        self.plot(c = self.C)

    def iterate_rgb(self):
        """
        Calculates the RGB values according to which point the step is
        travelling towards and which step it travelled towards last.
        """
        for i in range(1, len(self.N)):
            self.C[i,:] = (self.C[i-1] + self.r[self.N[i]])*0.5


@jit(cache=True, nopython=True)
def iterate_fast(corners, steps, points):
    """
    Function that increases the speed that the class iterates through points.

    corners: array containing the coordinates of the corners
    steps: how many steps to iterate for
    points: array should be of the shape (steps, 2), with (0,:) being the
            starting point
    """
    N = np.random.randint(0,3,steps)
    for i in range(1, steps):
        points[i] = (points[i-1] + corners[N[i]])*0.5

    return points, N

@jit(cache=True, nopython=True)
def iterate_rgb_fast(C, N, r):
    """
    Function that increases the speed that the class iterates through
    the RGB values
    """
    for i in range(1, len(N)):
        C[i] = (C[i-1] + r[N[i]])*0.5
    return C


if __name__=="__main__":
    T = Triangle()
    T.plot_triangle()
    T._starting_point()
    T.check_starting_point()
    T.iterate()
    T.plot()
    T.plot_color()
    T.plot_rbg()
