import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt


class Pendulum():
    """
    A class to represent a pendulum, with a completely rigid
    rod connecting it to the origin of our coordinate system.

    The pendulum hangs freely under gravity, air resistance and
    hinge friction is ignored. Thus the sum of Potential and
    Kinetic energy should remain constant.

    The total energy may drop over time, this is because the
    integration methods used in SciPy's solve_ivp are not
    perfect. Try a different integration method for solve_ivp
    if you experience significant total energy loss.

    Contains a method to solve an initial value problem for
    this pendulum.
    """

    def __init__(self, M = 1, L = 1, g = 9.81, method = "RK45"):
        """
        M: mass of the pendulum
        L: length of rod, connecting pendulum to origin
        g: gravitational constant
        method: which method SciPy's solve_ivp should utilise
                to solve the ivp.

        self.Solver_Run is a boolean which the check_run method
        uses to check whether the class instance has run the
        solve method.
        """
        self.M = M
        self.L = L
        self.g = g
        self.method = method
        self._Solver_Run = False

    def __call__(self, t, u):
        """
        Takes in tuple u = (theta_i, omega_i)
        Returns tuple u_d = (d_theta_i, d_omega_i)
        """

        d_theta = u[1]
        d_omega = -(self.g/self.L) * np.sin(u[0])
        return (d_theta, d_omega)

    def solve(self, y0, T, dt, angles = "rad"):
        """
        Solves an initial value problem for our pendulum.

        input
        y0: our initial values, use form: [theta_0, omega_0]
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
        self._theta = sol.y[0]
        self._omega = sol.y[1]

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
    def theta(self):
        "Angular displacement array for the pendulum"
        self.check_run()
        return self._theta

    @property
    def omega(self):
        "Angular velocity array for the pendulum"
        self.check_run()
        return self._omega

    @property
    def x(self):
        "Pendulum x-position over time"
        return self.L * np.sin(self._theta)

    @property
    def y(self):
        "Pendulum y-position over time"
        return - self.L * np.cos(self._theta)

    @property
    def vx(self):
        "Pendulum linear velocity in x-direction"
        return np.gradient(self.x, self._t)

    @property
    def vy(self):
        "Pendulum linear velocity in y-direction"
        return np.gradient(self.y, self._t)

    @property
    def potential(self):
        "Potential energy of the system"
        return self.M * self.g * (self.y + self.L)

    @property
    def kinetic(self):
        "Kinetic energy of the system"
        v_sq = self.vx**2 + self.vy**2
        return 0.5 * self.M * v_sq


class DampenedPendulum(Pendulum):
    """
    Inherits from the Pendulum class, contains all the same
    methods and properties, except the __call__ method has
    been modified to work with a dampening factor B.
    """

    def __init__(self, M = 1, L = 1, g = 9.81, B = 0.25, method = "RK45"):
        """
        See Pendulum __init__.

        B: dampening factor
        """
        Pendulum.__init__(self, M, L, g, method)
        self.B = B

    def __call__(self, t, u):
        """
        Takes in tuple u = (theta_i, omega_i)
        Returns tuple u_d = (d_theta_i, d_omega_i)
        """

        d_theta = u[1]
        d_omega = -(self.g/self.L) * np.sin(u[0]) - (self.B/self.M*u[1])
        return (d_theta, d_omega)



if __name__ == "__main__":

    # Energy Conserving Pendulum

    P1 = Pendulum(L = 2.7)#, method = "Radau")
    u0 = [np.pi/4, 0]
    T = 10
    dt = 1e-3
    P1.solve(u0,T,dt)

    plt.figure(1, figsize=(9,7))
    plt.plot(P1.t, P1.theta, "r", label=r"$\theta(t)$")
    plt.axhline(0, lw=0.25, c="k", ls="--")
    plt.title(r"$\theta(t)$")
    plt.xlabel(r"Time$_{\ (s)}$")
    plt.ylabel(r"$\theta_{(rad)}$")
    plt.legend()

    plt.figure(2, figsize=(9,7))
    plt.subplot(3,1,1)
    plt.plot(P1.t, P1.kinetic, "k")
    plt.axhline(0, lw=0.25, c="k", ls="--")
    plt.title(r"$Kinetic\ Energy\ of\ pendulum$")
    plt.xlabel(r"Time$_{\ (s)}$")
    plt.ylabel(r"Kinetic Energy")

    plt.subplot(3,1,2)
    plt.plot(P1.t, P1.potential, "r")
    plt.axhline(0, lw=0.25, c="k", ls="--")
    plt.title(r"$Potential\ Energy\ of\ pendulum$")
    plt.xlabel(r"Time$_{\ (s)}$")
    plt.ylabel(r"Potential Energy")

    plt.subplot(3,1,3)
    tot_en = (P1.kinetic + P1.potential)
    plt.plot(P1.t, tot_en, "b")
    plt.axhline(tot_en[0], lw=0.25, c="k", ls="--")
    plt.title(r"$Total\ Energy\ of\ pendulum$")
    plt.xlabel(r"Time$_{\ (s)}$")
    plt.ylabel(r"Total Energy")

    plt.tight_layout()

    plt.show()


    # Dampened Pendulum Plot

    P1 = DampenedPendulum(L = 2.7)
    u0 = [np.pi/4, 0]
    T = 10
    dt = 1e-3
    P1.solve(u0,T,dt)

    plt.figure(1, figsize=(9,7))
    plt.plot(P1.t, P1.theta, "r", label=r"$\theta(t)$")
    plt.axhline(0, lw=0.25, c="k", ls="--")
    plt.title(r"$\theta(t)$")
    plt.xlabel(r"Time$_{\ (s)}$")
    plt.ylabel(r"$\theta_{(rad)}$")
    plt.legend()

    plt.figure(2, figsize=(9,7))
    plt.subplot(3,1,1)
    plt.plot(P1.t, P1.kinetic, "k")
    plt.axhline(0, lw=0.25, c="k", ls="--")
    plt.title(r"$Kinetic\ Energy\ of\ pendulum$")
    plt.xlabel(r"Time$_{\ (s)}$")
    plt.ylabel(r"Kinetic Energy")

    plt.subplot(3,1,2)
    plt.plot(P1.t, P1.potential, "r")
    plt.axhline(0, lw=0.25, c="k", ls="--")
    plt.title(r"$Potential\ Energy\ of\ pendulum$")
    plt.xlabel(r"Time$_{\ (s)}$")
    plt.ylabel(r"Potential Energy")

    plt.subplot(3,1,3)
    tot_en = (P1.kinetic + P1.potential)
    plt.plot(P1.t, tot_en, "b")
    plt.axhline(tot_en[0], lw=0.25, c="k", ls="--")
    plt.title(r"$Total\ Energy\ of\ pendulum$")
    plt.xlabel(r"Time$_{\ (s)}$")
    plt.ylabel(r"Total Energy")

    plt.tight_layout()

    plt.show()
