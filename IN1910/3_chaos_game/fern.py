import numpy as np
import matplotlib.pyplot as plt
from os import path
from os import makedirs


class AffineTransform():
    """
    A simple class to perform an affine transformation on a 2D-vector
    This class is on the form:

        A*[x,y] = [(a*x + b*y + e), (c*x + d*y + f)]
    """

    def __init__(self, vals = [0,0,0,0,0,0]):

        self.a, self.b, self.c, self.d, self.e, self.f = vals

    def __call__(self, point=[0,0]):

        x = self.a*point[0] + self.b*point[1] + self.e
        y = self.c*point[0] + self.d*point[1] + self.f

        return [x, y]


class Fern():

    """
    A class to illustrate how complex patterns can emerge from a seemingly
    simple set of rules.

    We take in a list of functions values to use in the AffineTransform class,
    and make a dictionary with those functions, we also take in a list of
    probabilities that correspond to the probability that a specific
    AffineTransform functions is used for that step.
    """

    def __init__(self, func_vals, p_vals):
        """
        func_vals: a list of lists of values to use in the AffineTransform class
        p_vals: list of probabilities, each corresponding to how likely
                it should be to select a specific function to use for the
                next step in the iteration
        """
        msg1 = "Probability sum not 1"
        msg2 = "The number of functions and probabilities do not match"
        assert sum(p_vals) == 1, msg1
        assert len(func_vals) == len(p_vals), msg2

        self.functions = {}
        for i in range(len(func_vals)):
            self.functions[i] = AffineTransform(func_vals[i])

        self.p_cumulative = []
        for i in range(1,len(p_vals)):
            self.p_cumulative.append(sum(p_vals[0:i]))
        self.p_cumulative.append(sum(p_vals))
        self.p_cumulative = np.asarray(self.p_cumulative)

    def find_func(self, r_val):
        """
        Method to determine which function should be called depending on the
        randomly generated r_val
        """
        for j in range(len(self.p_cumulative)):
            if r_val < self.p_cumulative[j]:
                return self.functions[j]

    def iterate(self, steps=50000, p0=[0,0]):
        """
        Method to iterate the system

        steps: how many steps to run the iteration for
        p0: the starting point of the system

        The method sets up an array of zeros of the shape (steps, 2), sets the
        first value with p0, then draws steps random numbers between 0 and 1.

        The method then uses self.find_func(r_val) to figure out which function
        to apply to the last point to find the current point.
        """

        self.points = np.zeros((steps,2), dtype=np.float64)
        self.points[0] = p0
        self.r = np.random.random(steps)

        for i in range(1, steps):
            f = self.find_func(self.r[i])
            self.points[i] = f(self.points[i-1])

    def plot(self, color = "g", axis = "off", fig = True):
        """
        Method to plot the system.

        color: pyplot color to use in the plot
        axis: sets the axis of the coordinate system "on" or "off"
        fig: sets whether the function should initialise it's own figure
        """
        if fig == True:
            plt.figure(figsize=(9,7))
        plt.axis("equal")
        plt.axis(axis)
        plt.scatter(self.points[:,0], self.points[:,1], c = color, s = 0.1)
        plt.tight_layout()

    def savefig(self, filename, folder, color = "g",
                axis = "off", fig = True, dpi=400):
        """
        Saves the plotted figure in a subfolder
        """
        if (path.isdir("%s"%(folder)) == False):
            makedirs("%s"%(folder))

        self.plot(color = color, axis = axis, fig = fig)
        plt.savefig("%s/%s"%(folder, filename), dpi = dpi)
        plt.close()

    def show_fig(self, color = "g", axis = "off", fig = True):
        """
        Shows the plotted figure
        """
        self.plot( color = color, axis = axis, fig = fig)
        plt.show()
        plt.close()


if __name__=="__main__":

    f_1 = [0, 0, 0, 0.16, 0, 0]
    f_2 = [0.85, 0.04, -0.04, 0.85, 0, 1.60]
    f_3 = [0.20, -0.26, 0.23, 0.22, 0, 1.60]
    f_4 = [-0.15, 0.28, 0.26, 0.24, 0, 0.44]
    func_vals = [f_1, f_2, f_3, f_4]
    p_vals = [0.01, 0.85, 0.07, 0.07]

    fern = Fern(func_vals, p_vals)
    fern.iterate()
    fern.savefig("barnsley_fern", "figures")
