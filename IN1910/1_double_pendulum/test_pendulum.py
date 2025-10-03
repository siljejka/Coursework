import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt
from pendulum import Pendulum
import pytest


class TestPendulum():
    """
    Utilised to test the Pendulum class
    """

    def test_pendulum_call(self):
        """
        Checks that the __call__ method of Pendulum returns
        a precomputed, expected value.
        """
        omega = 0.15
        theta = np.pi/6

        tol = 1e-12
        exp_d_omega = -1.8166666
        exp_d_theta = omega
        P1 = Pendulum(L = 2.7)
        d_vals = P1(0,(theta, omega))

        msg = "__call__ returned unexpected value"

        assert (d_vals[0] - exp_d_theta) < tol, msg
        assert (d_vals[1] - exp_d_omega) < tol, msg

    def test_pendulum_at_rest(self):
        """
        Checks that the pendulum remains at rest when initialised
        at position theta=0 and with radial velocity omega=0.

        This test is independent of the solve method, and only checks
        that the __call__ method returns the correct values. It starts
        with angles = (0,0), and then updates these in the for loop
        with a call to __call__(0, angles), and then asserts that
        the angles are still (0,0).
        """
        angles = (0,0)
        tol = 1e-12

        pend = Pendulum()
        msg = "Pendulum did not remain at rest"

        for i in range(1000):
            angles = pend(0, angles)
            assert np.abs(angles[0]+angles[1]) < tol, msg

    def test_pendulum_solve(self):
        """
        Checks that the t, theta, omega, x, and y properties raise
        an AttributeError, because the solver has not been run yet.

        Then checks that the pendulum remains at rest, if the solver
        is run with the inital angles (0,0).

        Lastly checks that the time array it returns is correct.
        """
        P1 = Pendulum(L = 2.7)
        angles = (0,0)
        T = 10
        dt = 0.1
        tol = 1e-12

        with pytest.raises(AttributeError):
            P1.theta
            P1.omega
            P1.t
            P1.x
            P1.y

        P1.solve(angles,T,dt)
        thetas = np.sum(P1.theta)
        omegas = np.sum(P1.omega)

        msg_angle = "Pendulum did not remain at rest"

        assert (thetas+omegas) < tol, msg_angle

        msg_t = "Time array not correct"

        t = P1.t[0]
        for i in range(len(P1.t)):
            t = i*dt
            assert (t - P1.t[i]) < tol, msg_t

    def test_pendulum_range(self):
        """
        Checks that the pendulum length remains constant
        during a simulation.
        """
        P1 = Pendulum(L = 2.7)
        angles = (np.pi / 4, 0)
        T = 10
        dt = 0.1
        tol = 1e-12
        P1.solve(angles,T,dt)
        r = (P1.x)**2 + (P1.y)**2
        r_check = r - (P1.L)**2

        msg = "Pendulum length not correct"

        for radius in r_check:
            assert radius < tol, msg


if __name__ == "__main__":
    P_test = TestPendulum()

    P_test.test_pendulum_call()
    P_test.test_pendulum_at_rest()
    P_test.test_pendulum_solve()
    P_test.test_pendulum_range()
