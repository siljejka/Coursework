import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from double_pendulum import DoublePendulum


class AnimateDoublePendulum(DoublePendulum):
    """
    Inherits all functionality from the DoublePendulum class.

    This class is made to animate the solutions to the initial value problems
    we solve with the DoublePendulum class.
    """

    def __init__(self, M1 = 1, M2 = 1, L1 = 1, L2 = 1, g = 9.81,
                 method = "Radau", axis = "off", axis_scale = "equal",
                 axis_lim = (-2,2,-2.5,0.5),
                 auto_lim = True, fps = 60, inc_trace = False):

        """
        axis: string to set whether axes should be drawn
        axis_scale: string to set whether the axis should be scaled
                    equally in the x,y directions.
        axis_lim: tuple of 4 values, (x_min, x_max, y_min, y_max) to set
                  the axis limits.
        auto_lim: bool, if True it tries to automatically calculate
                  appropriate axis limits based on the highest/lowest
                  x and y coordinates the second pendulum reached.
        fps: sets the frames per second for the save_animation method,
             and the real_time_animation method.
        inc_trace: bool, sets whether the animation should include a
                   trace of the pendulums as they move.
        """

        DoublePendulum.__init__(self, M1, M2, L1, L2, g, method)
        self.axis = axis
        self.axis_scale = axis_scale
        self.axis_lim = axis_lim
        self.auto_lim = auto_lim
        self.fps = fps
        self.inc_trace = inc_trace

    def init_frame(self):
        """
        Initialises the frame of the animation.
        """
        fig = plt.figure(1, figsize=(7,7))
        plt.axis(self.axis_scale)
        plt.axis(self.axis)
        if self.auto_lim == False:
            plt.axis(self.axis_lim)
            self.timer_x = self.axis_lim[0]*1.25
            self.timer_y = self.axis_lim[2]*1.25
        else:
            x_max = np.max((np.abs(np.min(self.x_2)), np.abs(np.max(self.x_2))))
            self.timer_x = -x_max*1.25
            y_min = np.min(self.y_2)
            if np.max(self.y_2) >= 0:
                y_max = np.max(self.y_2)
                self.timer_y = y_max * 1.275
            else:
                y_max = 0
                self.timer_y = 0.1
            self.axis_lim = np.array([-x_max, x_max, y_min, y_max])*1.25
            plt.axis(self.axis_lim)

        plt.plot(0,0,"ro")
        return fig

    def _next_frame(self, i):
        """
        returns the next frame for the animation.
        Sets the data/text of the properties to the i'th value.
        """
        self.pendulum_1.set_data(self.x_1[i], self.y_1[i])
        self.pendulum_2.set_data(self.x_2[i], self.y_2[i])
        self.line_1.set_data([0,self.x_1[i]], [0,self.y_1[i]])
        self.line_2.set_data([self.x_1[i],self.x_2[i]],[self.y_1[i],self.y_2[i]])
        self.txt.set_text("t = %.2f"%(self.t[i]))
        return (self.pendulum_1, self.pendulum_2, self.line_1, self.line_2,
                self.txt, )

    def _next_frame_trace(self, i):
        """
        returns the next frame for the animation.
        Sets the data/text of the properties to the i'th value.

        This method also includes a trace, and sets the trace lines data
        from 0 to the i'th value.
        """
        self.pendulum_1.set_data(self.x_1[i], self.y_1[i])
        self.pendulum_2.set_data(self.x_2[i], self.y_2[i])
        self.line_1.set_data([0,self.x_1[i]], [0,self.y_1[i]])
        self.line_2.set_data([self.x_1[i],self.x_2[i]],[self.y_1[i],self.y_2[i]])
        self.trace_1.set_data(self.x_1[0:i], self.y_1[0:i])
        self.trace_2.set_data(self.x_2[0:i], self.y_2[0:i])
        self.txt.set_text("t = %.2f"%(self.t[i]))
        return (self.pendulum_1, self.pendulum_2, self.line_1, self.line_2,
                self.trace_1, self.trace_2, self.txt, )

    def create_animation(self, blit = True):
        """
        Creates an animation based on the current local stored solution, if
        the solver has not been run yet it raises an exception through
        check_run(), and saves the animation as a local variable of the
        class instance.

        Uses self.inc_trace to decide whether to use _next_frame or
        _next_frame_trace to draw the next frame.
        """

        self.check_run()

        self.anim = None

        dt = self.t[2] - self.t[1]
        frames = len(self.x_1)

        self.fig = self.init_frame()
        self.pendulum_1, = plt.plot([], [], c="r", marker="o", markersize=10)
        self.pendulum_2, = plt.plot([], [], c="r", marker="o", markersize=10)
        self.line_1, = plt.plot([], [], c = "k", ls = "-", lw = 0.5)
        self.line_2, = plt.plot([], [], c = "k", ls = "-", lw = 0.5)
        self.txt = plt.text(self.timer_x,self.timer_y,"t = 0")

        if self.inc_trace == True:
            self.trace_1, = plt.plot([], [], c = "b", ls = "--", lw = 0.5)
            self.trace_2, = plt.plot([], [], c = "b", ls = "--", lw = 0.5)
            anim_func = self._next_frame_trace
        else:
            anim_func = self._next_frame


        anim = animation.FuncAnimation(self.fig,
                                       func = anim_func,
                                       frames = frames,
                                       repeat = None,
                                       interval = 1000*dt,
                                       blit = blit)

        self.anim = anim


    def show_animation(self):
        """
        Calls the create_animation method and shows the animation using
        pyplot.show()
        """
        self.create_animation(blit = False)
        plt.show()
        plt.close(self.fig)

    def save_animation(self, filename = "Double_Pendulum", dpi = 400):
        """
        Calls the create_animation method and saves the animations as an mp4
        file.

        filename: Specifies the name of the saved animation, "filename.mp4"
        dpi: specifies the dots-per-inch to be drawn in the savefile.
        """
        self.create_animation()
        self.anim.save("%s.mp4" %(filename),
                       writer = "ffmpeg", fps = self.fps,
                       dpi = dpi)
        plt.close(self.fig)

    def real_time_animation(self, y0, T, angles = "rad", vid_speed = 1):
        """
        Extra method, included to run the solver with a dt that ensures the
        simulation is rendered in real time, in relation to the fps it will be
        saved with.

        y0: our initial values, use form: [theta_0, omega_0, theta_1, omega_1]
        T: total time to solve for
        dt: timestep to use when solving
        angles: string to denote whether the inital values
                are given in radians or degrees
        """
        dt = (vid_speed/self.fps)
        self.solve(y0, T, dt, angles)




if __name__ == "__main__":

    P_dub = AnimateDoublePendulum(inc_trace = True, axis = "off")
    P_dub.real_time_animation(y0 = (np.pi/4, 2*np.pi, 0, -4*np.pi), T = 10)
    P_dub.save_animation(filename= "example_simulation",)
    P_dub.show_animation()
