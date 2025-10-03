import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib as mpl
from os import path
from os import makedirs

from chaos_game import ChaosGame
from fern import AffineTransform, Fern


class Variations():
    """
    A class which does a transformation on the space, changing the shape of
    figures within it.
    """

    def __init__(self, x, y, colors = "black"):
        """
        x: array containing the x-coordinates of the points
        y: array containing the y-coordinates of the points
        tol: a small value we add to r in order to avoid ZeroDivision errors
        """
        max = np.max([np.abs(x), np.abs(y)])
        if max > 1:
            self.x = x / max
            self.y = y / max
        else:
            self.x, self.y = x, y
        self.tol = 1e-12

        self.r = np.sqrt(x**2 + y**2)
        self.theta = np.arctan2(x, y)

        self.colors = colors
        self.implemented_variations = ["linear", "handkerchief", "swirl",
                                       "disc", "sinusoidal", "horseshoe",
                                       "polar", "spiral", "hyperbolic",
                                       "diamond", "ex", "fisheye",
                                       "exponential", "cosine", "bubble"]

    def __call__(self, coeff_dict):
        """
        coeff_dict: Dictionary with implemented variations as keys and
                    their corresponding weights as values

        Creates a linear combination of the given variations in the coefficient
        dictionary.
        """
        msg = "Sum of coefficients not 1"
        s = 0
        for key in coeff_dict:
            s += coeff_dict[key]
        assert s == 1, msg

        self.lin_u = np.zeros(len(self.x))
        self.lin_v = np.zeros(len(self.y))

        for key in coeff_dict:
            self.call_method_str(key)
            self.lin_u += self.u*coeff_dict[key]
            self.lin_v += self.v*coeff_dict[key]

        self.u = self.lin_u.copy()
        self.v = self.lin_v.copy()

    def linear(self):
        """
        Creates the linear variation
        """
        self.u, self.v = self.x, self.y

    def handkerchief(self):
        """
        Creates the handkerchief variation
        """
        self.u = self.r * np.sin(self.theta + self.r)
        self.v = self.r * np.cos(self.theta - self.r)

    def swirl(self):
        """
        Creates the swirl variation
        """
        self.u = self.x * np.sin(self.r**2) - self.y * np.cos(self.r**2)
        self.v = self.x * np.cos(self.r**2) + self.y * np.sin(self.r**2)

    def disc(self):
        """
        Creates the disc variation
        """
        self.u = (self.theta/np.pi) * np.sin(np.pi * self.r)
        self.v = (self.theta/np.pi) * np.cos(np.pi * self.r)

    def sinusoidal(self):
        """
        Creates the sinusoidal variation
        """
        self.u = np.sin(self.x)
        self.v = np.sin(self.y)

    def horseshoe(self):
        """
        Creates the horseshoe variation
        """
        self.u = (1/(self.r + self.tol)) * (self.x - self.y) * (self.x + self.y)
        self.v = (1/(self.r + self.tol)) * 2 * self.x * self.y

    def polar(self):
        """
        Creates the polar variation
        """
        self.u = self.theta
        self.v = self.r - 1

    def spiral(self):
        """
        Creates the spiral variation
        """
        self.u = (1/(self.r + self.tol)) * (np.cos(self.theta) + np.sin(self.r))
        self.v = (1/(self.r + self.tol)) * (np.sin(self.theta) - np.cos(self.r))

    def hyperbolic(self):
        """
        Creates the hyperbolic variation
        """
        self.u = np.sin(self.theta) / (self.r + self.tol)
        self.v = self.r * np.cos(self.theta)

    def diamond(self):
        """
        Creates the diamond variation
        """
        self.u = np.sin(self.theta) * np.cos(self.r)
        self.v = np.cos(self.theta) * np.sin(self.r)

    def ex(self):
        """
        Creates the ex variation
        """
        p_0 = np.sin(self.theta + self.r)
        p_1 = np.cos(self.theta - self.r)

        self.u = self.r * (p_0**3 + p_1**3)
        self.v = self.r * (p_0**3 - p_1**3)

    def fisheye(self):
        """
        Creates the fisheye variation
        """
        self.u = (2 / (self.r + 1)) * self.y
        self.v = (2 / (self.r + 1)) * self.x

    def exponential(self):
        """
        Creates the exponential variation
        """
        self.u = np.exp(self.x - 1) * np.cos(np.pi * self.y)
        self.v = np.exp(self.x - 1) * np.sin(np.pi * self.y)

    def cosine(self):
        """
        Creates the cosine variation
        """
        self.u = np.cos(np.pi * self.x) * np.cosh(self.y)
        self.v = -np.sin(np.pi * self.x) * np.sinh(self.y)

    def bubble(self):
        """
        Creates the bubble variation
        """
        self.u = (4/(self.r**2 + 4)) * self.x
        self.v = (4/(self.r**2 + 4)) * self.y

    def call_method_str(self, method):
        """
        Takes in a string with the same name as a method, checks if it
        is implemented, and if it is it calls that method.
        """
        if method not in self.implemented_variations:
            raise NotImplemented("This method is not implemented")
        else:
            getattr(self, method)()

    def plot(self, cmap="cividis_r", axis = "off", fig = True,
             force_limits = False):
        """
        Plots the currently calculated u and v arrays
        """
        if fig == True:
            plt.figure(figsize=(9,7))
        plt.axis("equal")
        plt.axis(axis)

        if force_limits == True:
            if min(self.u) < -2 or max(self.u) > 2:
                plt.axis([-2, 2, -2, 2])
            elif min(self.v) < -2 or max(self.v) > 2:
                plt.axis([-2, 2, -2, 2])

        plt.scatter(self.u, -self.v, c=self.colors, cmap=cmap, s=0.1)
        plt.tight_layout()

    def savefig(self, method, filename, folder, dpi=400):
        """
        Creates a variation with call_method_str(method), plots it and
        saves it as a png
        """
        self.call_method_str(method)
        self.plot()
        plt.savefig("%s/%s_%s.png"%(folder, filename, method), dpi = dpi)
        plt.close()

    def plot_all_variations(self, filename, folder, dpi=400):
        """
        Plots all available variations.
        """
        if (path.isdir("%s"%(folder)) == False):
            makedirs("%s"%(folder))
        for method in self.implemented_variations:
            self.savefig(method, filename, folder, dpi)

    def calc_transform(self, n = 200, variations = ["disc", "horseshoe"]):
        """
        Does the calculations for an Ax -> Bx transformation. This can be done
        for any number of transformations, ie:
            A1*X +
        """
        self.variations_combinations = {}
        for i in range(0, (len(variations)-1)):
            var_dict = {}
            vals = np.linspace(0,1,n)
            for j in range(n):
                var_dict[j] = {variations[i]: 1-vals[j], \
                               variations[i+1]: vals[j]}
                #print(var_dict[j])
            self.variations_combinations[i] = var_dict

        N = len(variations)-1
        self.xy_vals = np.zeros((n*N, len(self.x), 2))
        self.methods = np.empty(n*N, dtype=object)

        count = 0
        for key in self.variations_combinations:
            for i in range(n):
                self.__call__(self.variations_combinations[key][i])
                self.xy_vals[count*n + i, :, 0] = self.u
                self.xy_vals[count*n + i, :, 1] = -self.v
                transition = ""
                for method in self.variations_combinations[key][i]:
                    transition += method + " to "
                self.methods[count*n + i] = "%s"%(transition[0:-3])
            count += 1

    def calc_cumulative_transform(self, n = 200, start_var = "linear",
                                  variations=["exponential","handkerchief"]):
        """
        Performs an X -> A1*X -> A1*A2*X -> A1*A2*...*An*X calculation

        Sets up a nested dictionary of the variations we wish to transition
        between, it first sets the outer dict to be {var1, var2, ...}, then the
        dict for var1 looks like {1,2,3,...,n}, and each value within that is a
        dict of the form {var1: omega_n, linear: 1-omega_n}, where omega are
        n linearly spaced values between 0 and 1.

        It then calculates the appropriate for each linearly spaced inner
        dictionary, and stores them locally, after it has finished calculating
        for var1, it sets the internal "x" and "y" values to the last calculated
        "u" and "v" values, so that the calculation can progress from the
        finished linear transformation, and proceeds to repeat the process
        for any remaining variables.
        """
        self.call_method_str(start_var)
        self.x = self.u
        self.y = self.v

        self.variation_dict = {}
        for var in variations:
            var_dict = {}
            vals = np.linspace(0,1,n)
            for i in range(n):
                var_dict[i] = {var: vals[i], "linear": (1-vals[i])}

            self.variation_dict[var] = var_dict

        N = len(variations)
        self.xy_vals = np.zeros((n*N, len(self.x) ,2))
        self.methods = np.empty(n*N, dtype=object)

        count = 0
        for key in self.variation_dict:
            for i in range(n):
                self.__call__(self.variation_dict[key][i])
                self.xy_vals[count*n + i, :, 0] = self.u
                self.xy_vals[count*n + i, :, 1] = -self.v
                self.methods[count*n + i] = "%s"%(key)
            self.x = self.u
            self.y = self.v
            count += 1

    def _setup_frame(self, lims):
        """
        Sets up the frame of the animation
        """
        fig = plt.figure(1, figsize=(9,7))
        #plt.axis('equal')
        plt.axis(lims)
        plt.axis('on')
        return fig

    def _next_frame_colors(self, i):
        """
        Gets the data for the next frame of the animation,
        and sets the color data
        """
        self.anim_xy.set_offsets(self.xy_vals[i])
        self.anim_xy.set_facecolors(self.colors_rgba)
        self.txt.set_text("%s"%(self.methods[i]))
        return (self.anim_xy, )

    def _next_frame(self, i):
        """
        Gets the data for the next frame of the animation
        """
        self.anim_xy.set_offsets(self.xy_vals[i])
        self.txt.set_text("%s"%(self.methods[i]))
        return (self.anim_xy, )

    def animate_variation(self, blit = True, filename="anim_test",
                          fps=60, dpi=400, lims = (-1, 1, -1, 1)):
        """
        Animates the variations with data from calc_transform or
        calc_cumulative_transform.
        """

        self.fig = self._setup_frame(lims)
        self.txt = plt.text(lims[0]*0.8, lims[3]*0.8, "")

        if isinstance(self.colors, str):
            anim_func = self._next_frame
            self.anim_xy = plt.scatter([], [], c=self.colors, marker=".", s=0.01)
        else:
            N = mpl.colors.Normalize(vmin = min(self.colors), vmax = max(self.colors))
            self.m = mpl.cm.ScalarMappable(norm = N)
            self.colors_rgba = self.m.to_rgba(self.colors)
            anim_func = self._next_frame_colors
            self.anim_xy = plt.scatter([], [], c="k", marker=".", s=0.01)

        frames = len(self.xy_vals)
        dt = 1

        self.anim = animation.FuncAnimation(self.fig, func=anim_func,
                                            frames = frames, repeat = None,
                                            interval = dt, blit = blit)

        #plt.show()
        self.anim.save("%s.mp4" %(filename),
                       writer = "ffmpeg", fps = fps,
                       dpi = dpi)
        plt.clf()
        plt.close()


def setup_class_instance(colors = "green"):
    f_1 = [0, 0, 0, 0.16, 0, 0]
    f_2 = [0.85, 0.04, -0.04, 0.85, 0, 1.60]
    f_3 = [0.20, -0.26, 0.23, 0.22, 0, 1.60]
    f_4 = [-0.15, 0.28, 0.26, 0.24, 0, 0.44]
    func_vals = [f_1, f_2, f_3, f_4]
    p_vals = [0.01, 0.85, 0.07, 0.07]
    F = Fern(func_vals, p_vals)
    F.iterate()
    max = np.max([np.max(np.abs(F.points[:,0])), np.max(np.abs(F.points[:,1]))])
    x = F.points[:,0] / max
    y = F.points[:,1] / max
    V = Variations(x, -y, colors = colors)
    return V

def task_4c():

    var = setup_class_instance(colors = "green")
    var.plot_all_variations("fern", "fern_figures")

    CG1 = ChaosGame(n=3, r=0.5)
    CG2 = ChaosGame(n=6, r=1./3)
    CG3 = ChaosGame(n=7, r=1./3)

    CG1._starting_point()
    CG2._starting_point()
    CG3._starting_point()

    CG1.iterate(steps=int(1e6))
    CG2.iterate(steps=int(1e6))
    CG3.iterate(steps=int(1e6))

    Var1 = Variations(CG1_x, -CG1_y, colors = CG1._compute_color())
    Var2 = Variations(CG2_x, -CG2_y, colors = CG2._compute_color())
    Var3 = Variations(CG3_x, -CG3_y, colors = CG3._compute_color())

    Var1.plot_all_variations("3gon", "n_gon_figures")
    Var2.plot_all_variations("6gon", "n_gon_figures")
    Var3.plot_all_variations("7gon", "n_gon_figures")

def task_4d_fern(steps=1e5):

    var = setup_class_instance(colors = "green")

    N = 4
    coeff = np.linspace(1,0,N)
    coeff_dict = {}

    plt.figure(figsize=(9,9))
    for i in range(N):
        plt.subplot(2, 2, i+1)
        coeff_dict["linear"] = coeff[i]
        coeff_dict["swirl"] = 1 - coeff[i]
        var(coeff_dict)
        var.plot(fig = False)

    plt.tight_layout()
    plt.show()
    plt.close()

def task_4d_ngon(n=3, r=0.5, steps=1e6):
    CG = ChaosGame(n=n, r=r)
    CG._starting_point()
    CG.iterate(steps=int(steps))

    var = Variations(CG.points[:,0], -CG.points[:,1],
                     colors = CG._compute_color())

    N = 4
    coeff = np.linspace(1,0,N)
    coeff_dict = {}

    plt.figure(figsize=(9,9))
    for i in range(N):
        plt.subplot(2, 2, i+1)
        coeff_dict["disc"] = coeff[i]
        coeff_dict["horseshoe"] = 1 - coeff[i]
        var(coeff_dict)
        var.plot(cmap = "rainbow", fig = False)

    plt.tight_layout()
    plt.show()
    plt.close()

def task_4e_1():
    vars=["exponential", "cosine", "fisheye", "handkerchief"]
    start_var = "linear"
    lims = (-1.5, 1.5, -1.5, 1.5)
    V = setup_class_instance()
    V.colors = "green"
    V.calc_cumulative_transform(variations=vars, start_var = start_var)
    V.animate_variation(filename = "cumulative_transform", lims = lims)


def task_4e_2():
    vars=["disc", "horseshoe", "swirl", "cosine", "exponential", "ex"]
    CG = ChaosGame(n=3, r=0.5)
    CG._starting_point()
    CG.iterate(steps=int(1e5))
    lims = (-1.5, 1.5, -1.5, 1.5)

    var = Variations(CG.points[:,0], -CG.points[:,1],
                     colors = CG._compute_color())

    var.calc_transform(variations = vars)
    var.animate_variation(filename = "triangle_transform", lims = lims)

if __name__=="__main__":

    task_4c()
    task_4d_fern()
    task_4d_ngon()
    task_4e_1()
    task_4e_2()
