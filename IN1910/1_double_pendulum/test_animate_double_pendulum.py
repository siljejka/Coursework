import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt
from double_pendulum import DoublePendulum
from animate_double_pendulum import AnimateDoublePendulum
import pytest


class TestAnimateDoublePendulum():
    """
    Utilised to test the AnimateDoublePendulum class, basically a carbon copy
    of TestDoublePendulum, but utilised to make sure everything is inherited
    correctly.
    """

    def test_at_rest(self):
        """
        Checks that the system remains at rest given the inital angles
        (0,0,0,0).

        Then checks that the time array it returns is correct.
        """
        P_dub = AnimateDoublePendulum()
        angles = [0, 0, 0, 0]
        T = 10
        dt = 0.01
        tol = 1e-12

        P_dub.solve(angles, T, dt)
        thetas = np.sum(P_dub.theta_1) + np.sum(P_dub.theta_2)
        omegas = np.sum(P_dub.omega_1) + np.sum(P_dub.omega_2)

        msg_angle = "Double pendulum system did not remain at rest"
        assert (thetas + omegas) < tol, msg_angle

        t = P_dub.t[0]
        msg_t = "Time array not correct"
        for i in range(len(P_dub.t)):
            t = i*dt
            assert (t - P_dub.t[i]) < tol, msg_t

    def test_range(self):
        """
        Checks that the pendulum lengths remains constant
        during a simulation.
        """
        P_dub = AnimateDoublePendulum()
        angles = [np.pi / 4, 0, 0, 0]
        T = 10
        dt = 0.01
        tol = 1e-6

        P_dub.solve(angles, T, dt)
        r1_sqr = (P_dub.x_1)**2 + (P_dub.y_1)**2
        r2_sqr = (P_dub.x_2 - P_dub.x_1)**2 + (P_dub.y_2 - P_dub.y_1)**2

        r1_check = r1_sqr - (P_dub.L1)**2
        r2_check = r2_sqr - (P_dub.L2)**2

        msg1 = "First pendulum length not correct"
        msg2 = "Second pendulum length not correct"

        for i in range(len(r1_check)):
            assert r1_check[i] < tol, msg1
            assert r2_check[i] < tol, msg2

    def test_property_assertion(self):
        """
        Checks that the t, thetas, omegas, Potential and Kinetic properties
        raise an AttributeError, because the solver has not been run.
        """
        P_dub = AnimateDoublePendulum()

        with pytest.raises(AttributeError):
            P_dub.t
            P_dub.theta_1
            P_dub.theta_2
            P_dub.omega_1
            P_dub.omega_2
            P_dub.Potential
            P_dub.Kinetic

if __name__ == "__main__":

    P_test = TestAnimateDoublePendulum()
    P_test.test_at_rest()
    P_test.test_range()
    P_test.test_property_assertion()
