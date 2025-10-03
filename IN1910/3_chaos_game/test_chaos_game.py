import numpy as np
import matplotlib.pyplot as plt
from numba import jit
import pytest
from chaos_game import ChaosGame


class TestChaosGame():
    """
    Utilised to test the ChaosGame class
    """
    def task_2c_plot(self, n = 5, N = 1000):
        """
        Visual check that starting points are within the n-gon.
        """
        CG = ChaosGame(n = n)

        plt.figure(figsize=(7,7))

        plt.plot(self.corners[:,0], self.corners[:,1], "k--", lw=0.5)
        plt.plot([self.corners[-1][0], self.corners[0][0]],
                 [self.corners[-1][1], self.corners[0][1]], "k--", lw=0.5)
        plt.scatter(self.corners[:,0], self.corners[:,1], c="k")

        for i in range(N-1):
            CG._starting_point()
            plt.plot(CG.start[0], CG.start[1], "b.")

        plt.show()
        plt.clf()

    def test_starting_points(self, n = 3, N=1000):
        """
        Initialises an n-gon, then finds the functions F for the lines through
        its corners. The test then generates N random starting points.

        For each line the range of x-values between the corners the line was
        derived from is found. The y-intercept is then used to check whether
        the points should be above or below this line.

        Then a boolean array is set up which is True if the x-value of the
        point is within this range. These values are then used to check if F of
        the points' x-values are above/below the points' y-values.
        """
        CG = ChaosGame(n = n)
        lines = {}
        for i in range(n):
            lines["Line_%d"%(i)] = find_line(CG.corners[i-1], CG.corners[i])

        start_points = np.zeros((N+1,2))
        for i in range(N):
            CG._starting_point()
            start_points[N] = CG.start

        for i in range(n):
            if lines["Line_%d"%(i)][0] == 0:
                pass
            else:
                f = lines["Line_%d"%(i)][0]
                x0, x1 = CG.corners[i-1,0], CG.corners[i, 0]

                if (lines["Line_%d"%(i)][2] > 0):
                    points_in = np.logical_and((start_points[:,0]>x0),
                                               (start_points[:,0]<x1))
                    checks = (f(start_points[points_in,:][:,0]) >
                                start_points[points_in,:][:,1])

                elif (lines["Line_%d"%(i)][2] < 0):
                    points_in = np.logical_and((start_points[:,0]<x0),
                                               (start_points[:,0]>x1))
                    checks = (f(start_points[points_in,:][:,0]) <
                                start_points[points_in,:][:,1])

                assert checks.all() == True

    def test_iterations(self, n = 3, N=1000):
        """
        Initialises an n-gon, then finds the functions F for the lines through
        its corners. The test chooses a random starting point and iterates
        through N steps.

        For each line the range of x-values between the corners the line was
        derived from is found. The y-intercept is then used to check whether
        the points should be above or below this line.

        Then a boolean array is set up which is True if the x-value of the
        point is within this range. These values are then used to check if F of
        the points' x-values are above/below the points' y-values.
        """
        CG = ChaosGame(n = n)
        lines = {}
        for i in range(n):
            lines["Line_%d"%(i)] = find_line(CG.corners[i-1], CG.corners[i])

        CG._starting_point()
        CG.iterate(steps = N)

        for i in range(n):
            if lines["Line_%d"%(i)][0] == 0:
                pass
            else:
                f = lines["Line_%d"%(i)][0]
                x0, x1 = CG.corners[i-1,0], CG.corners[i, 0]

                if (lines["Line_%d"%(i)][2] >0):
                    points_in = np.logical_and((CG.points[:,0]>x0),
                                            (CG.points[:,0]<x1))
                    checks = (f(CG.points[points_in,:][:,0]) >
                                CG.points[points_in,:][:,1])

                elif (lines["Line_%d"%(i)][2] < 0):
                    points_in = np.logical_and((CG.points[:,0]<x0),
                                            (CG.points[:,0]>x1))
                    checks = (f(CG.points[points_in,:][:,0]) <
                                CG.points[points_in,:][:,1])

                assert checks.all() == True

    def test_corner_distance(self, steps = 100):
        """
        Checks that all corners are at an equal distance from the next point,
        and that all corners are one unit from the origin.
        """
        n_vals = np.random.randint(3,100,steps)
        for N in n_vals:
            CG = ChaosGame(n=N)
            lengths = np.zeros(N)
            r = np.zeros(N)

            for i in range(len(CG.corners)):
                dx = CG.corners[i-1][0] - CG.corners[i][0]
                dy = CG.corners[i-1][1] - CG.corners[i][1]
                lengths[i] = np.sqrt(dx**2 + dy**2)
                r[i] = np.sqrt(CG.corners[i][0]**2 + CG.corners[i][1]**2)

            check_len = (lengths - lengths[0] < 1e-12)
            check_dist = (r - 1 < 1e-12)
            assert check_len.all(), "Lengths not equal"
            assert check_dist.all(), "Corners are not 1 unit away from origin"

    def test_errors(self):
        """
        Tests if ValueError is raised when n-values and r-values are outside
        of the range, and if an Exception is raised when the filename isn't
        png.
        """
        n_vals = [2, 3.5, 4.01]
        r_vals = [-0.5, 0, 1, 5]

        for N in n_vals:
            with pytest.raises(ValueError):
                CG = ChaosGame(n=N)
        for R in r_vals:
            with pytest.raises(ValueError):
                CG = ChaosGame(r=R)
        with pytest.raises(Exception):
            CG = ChaosGame()
            CG._starting_point()
            CG.iterate(steps = int(1e3))
            CG.savepng("filename.type")


def find_line(p1, p2):
    """
    Function to find the function of the line through two points, returns the
    function, gradient, and y-intercept. Approximates as a straight line through
    the x-axis if the y-intercept is above 100, and returns 0 for all.
    """
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = (p1[1] - m*p1[0])
    if (b < 100):
        return (lambda x: (m*x) + b, m, b)
    else:
        return [0,0,0]


if __name__=="__main__":

    test1 = TestChaosGame()
    #test1.task_2c_plot()

    test1.test_starting_points()
    test_ns = [3,4,5,6,7,10,20,25]
    for n in test_ns:
            test1.test_iterations(n = n)
            test1.test_starting_points(n = n)
    test1.test_corner_distance()
    test1.test_errors()
