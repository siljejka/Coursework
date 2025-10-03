import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt


class ExponentialDecay():
    """
    A simple class to model exponential decay.
    """

    def __init__(self,a):
        """
        a is the factor by which the value decays
        """
        self.a = a

    def __call__(self, t, u):
        """
        returns how much the system has decayed this step.
        t is unused, but required for SciPy's solve_ivp function

        u = current state of value
        """
        return (-self.a * u)

    def solve(self, u0, T, dt):
        """
        Solves an exponential decay problem with initial
        values u0, over time T, with timestep dt.

        u0: singular start value
        T: total time to run
        dt: timestep

        returns
        sol.t: an array of time values from 0 to T, with step dt
        sol.y[0]: the solved system values
        """
        t_vals = np.linspace(0,T,int(T/dt)+1)
        sol = spi.solve_ivp(self.__call__, [0,T], u0, method='RK45',
                            t_eval=t_vals)

        return sol.t, sol.y[0]




if __name__ == "__main__":

    a_vals = [0.95, 0.75, 0.5]
    u0 = [100]
    T = 20
    dt = 1e-3

    col = ["k", "b", "g", "r"]

    plt.figure(figsize = (9,7))
    plt.title("Exponential Decay Example")
    plt.xlabel("Time")
    plt.ylabel("Value")

    for i in range(len(a_vals)):
        ED = ExponentialDecay(a_vals[i])
        t, u = ED.solve(u0,T,dt)
        plt.plot(t, u, lw=0.5, c = col[i], ls="--")

    plt.show()
