import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt

class DoublePendulum():
    """
    A class to represent a pair of interconnected pendulums, with completely
    rigid rods. The first pendulum is connected to the origin of our coordinate
    system, and the second pendulum is connected to the first.

    The pendulums hangs freely under gravity, the interactions between the
    pendulums are accounted for but, air resistance and hinge friction is
    ignored. Thus the sum of Potential and Kinetic energy should remain constant.

    The total energy may drop over time, this is because the
    integration methods used in SciPy's solve_ivp are not
    perfect. Try a different integration method for solve_ivp
    if you experience significant total energy loss.

    Contains a method to solve an initial value problem for this system.
    """

    def __init__(self, M1 = 1, M2 = 1, L1 = 1, L2 = 1, g = 9.81, method = "Radau"):
        """
        M1, M2: Mass of the first pendulum, mass of the second pendulum
        L1, L2: Length of the first pendulum, length of the second pendulum
        g: gravitational constant
        method: which method SciPy's solve_ivp should utilise
                to solve the ivp.

        self.Solver_Run is a boolean which the check_run method
        uses to check whether the class instance has run the
        solve method.
        """
        self.M1, self.M2 = M1, M2
        self.L1, self.L2 = L1, L2
        self.g = g
        self.method = method
        self._Solver_Run = False

    def __call__(self, t, u):
        """
        Takes in tuple u = (theta_1, omega_1, theta_2, omega_2)
        Returns tuple u_d = (d_theta_1, d_omega_1, d_theta_2, d_omega_2)
        """

        com_M = self.M1 + self.M2
        del_theta = u[2] - u[0]
        sin_cos = np.sin(del_theta) * np.cos(del_theta)

        num1 = (self.M2 * self.L1 * u[1]**2 * sin_cos
                + self.M2 * self.g * np.sin(u[2]) * np.cos(del_theta)
                + self.M2 * self.L2 * u[3]**2 * np.sin(del_theta)
                - com_M * self.g * np.sin(u[0]))

        den1 = (com_M * self.L1
                - self.M2 * self.L1 * np.cos(del_theta)**2)

        num2 = (- self.M2 * self.L2 * u[3]**2 * sin_cos
                + com_M * self.g * np.sin(u[0]) * np.cos(del_theta)
                - com_M * self.L1 * u[1]**2 * np.sin(del_theta)
                - com_M * self.g * np.sin(u[2]))

        den2 = (com_M * self.L2
                - self.M2 * self.L2 * np.cos(del_theta)**2)

        d_theta_1, d_theta_2 = u[1], u[3]
        d_omega_1 = num1 / den1
        d_omega_2 = num2 / den2

        return (d_theta_1, d_omega_1, d_theta_2, d_omega_2)

    def solve(self, y0, T, dt, angles = "rad"):
        """
        Solves an initial value problem for our system of pendulums.

        input
        y0: our initial values, use form: [theta_0, omega_0, theta_1, omega_1]
        T: total time to solve for
        dt: timestep to use when solving
        angles: string to denote whether the inital values
                are given in radians or degrees

        output
        none, the method does not output any values, but
        stores the results as local variables of the instance.
        """

        if angles == "deg":
            y0 = np.deg2rad(y0)
        elif angles == "rad":
            pass
        else:
            raise Exception("Angles have to be in rad or deg.")

        t_vals = np.linspace(0, T, int(T/dt)+1)
        sol = spi.solve_ivp(self.__call__, (0, T), y0, method=self.method,
                                 t_eval=t_vals)

        self._Solver_Run = True
        self._t = sol.t
        self._theta_1 = sol.y[0]
        self._omega_1 = sol.y[1]
        self._theta_2 = sol.y[2]
        self._omega_2 = sol.y[3]

    def check_run(self):
        """
        Checks whether the solve method has been run,
        used by the properties to make sure they raise
        an exception if the solve method has not been run.
        """
        if self._Solver_Run == False:
            raise AttributeError("Solver not run")

    @property
    def t(self):
        "Time array"
        self.check_run()
        return self._t

    @property
    def theta_1(self):
        "Angular displacement array for the first pendulum"
        self.check_run()
        return self._theta_1

    @property
    def omega_1(self):
        "Angular velocity array for the first pendulum"
        self.check_run()
        return self._omega_1

    @property
    def theta_2(self):
        "Angular displacement array for the second pendulum"
        self.check_run()
        return self._theta_2

    @property
    def omega_2(self):
        "Angular velocity array for the second pendulum"
        self.check_run()
        return self._omega_2

    @property
    def x_1(self):
        "First pendulum x-position over time"
        return self.L1 * np.sin(self._theta_1)

    @property
    def y_1(self):
        "First pendulum y-position over time"
        return - self.L1 * np.cos(self._theta_1)

    @property
    def x_2(self):
        "Second pendulum x-position over time"
        return self.x_1 + self.L2 * np.sin(self._theta_2)

    @property
    def y_2(self):
        "Second pendulum y-position over time"
        return self.y_1 - self.L2 * np.cos(self._theta_2)

    @property
    def vx_1(self):
        "First pendulum linear velocity in x-direction"
        return np.gradient(self.x_1, self._t)

    @property
    def vy_1(self):
        "First pendulum linear velocity in y-direction"
        return np.gradient(self.y_1, self._t)

    @property
    def vx_2(self):
        "Second pendulum linear velocity in x-direction"
        return np.gradient(self.x_2, self._t)

    @property
    def vy_2(self):
        "Second pendulum linear velocity in y-direction"
        return np.gradient(self.y_2, self._t)

    @property
    def Potential_1(self):
        "Potential energy of first pendulum"
        return self.M1 * self.g * (self.y_1 + self.L1)

    @property
    def Potential_2(self):
        "Potential energy of second pendulum"
        return self.M2 * self.g * (self.y_2 + self.L1 + self.L2)

    @property
    def Potential(self):
        "Potential energy of system"
        return self.Potential_1 + self.Potential_2

    @property
    def Kinetic_1(self):
        "Kinetic energy of first pendulum"
        v1_sq = self.vx_1**2 + self.vy_1**2
        return 0.5 * self.M1 * v1_sq

    @property
    def Kinetic_2(self):
        "Kinetic energy of second pendulum"
        v2_sq = self.vx_2**2 + self.vy_2**2
        return 0.5 * self.M2 * v2_sq

    @property
    def Kinetic(self):
        "Kinetic energy of system"
        return self.Kinetic_1 + self.Kinetic_2



if __name__ == "__main__":

    P_dub = DoublePendulum(method= "Radau")
    u0 = (np.pi/4, 0, 0, 0)
    T = 10
    dt = 1e-3

    P_dub.solve(u0, T, dt)

    plt.figure(1, figsize=(9,7))
    plt.plot(P_dub._t, P_dub._theta_1)
    plt.plot(P_dub._t, P_dub._theta_2)
    plt.show()

    plt.figure(2, figsize=(9,7))
    plt.plot(P_dub._t, P_dub.Kinetic)
    plt.plot(P_dub._t, P_dub.Potential)
    plt.plot(P_dub._t, P_dub.Kinetic + P_dub.Potential)

    plt.show()
