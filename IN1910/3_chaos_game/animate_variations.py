import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from matplotlib import animation

from chaos_game import ChaosGame
from fern import AffineTransform, Fern
from variations import Variations


class AnimateVariations():

    def __init__(self, points, steps = 1e4, color = False, colors = "black",
                 cmap = "rainbow", dpi = 400, methods = ["disc", "horseshoe"]):

        self.steps = int(steps)
        self.color = color
        self.colors = colors
        self.cmap = cmap
        self.dpi = dpi

        self.var = Variations(points[0], -points[1], colors = colors)
        self.methods = methods
        self.n = len(methods)
        self.coeff = np.linspace(1,0,self.steps)

        self._transition()

    def init_frame(self):

        fig = plt.figure(figsize=(9,7))
        plt.axis("equal")
        plt.axis("off")

        return fig

    def _transition(self):

        coeff_dict = {}
        self.uv_vals = np.zeros(((self.n-1)*self.steps, len(self.var.x), 2))

        for j in range(self.n-1):
            for i in range(self.steps):
                coeff_dict[self.methods[j]] = self.coeff[i]
                coeff_dict[self.methods[j+1]] = 1 - self.coeff[i]
                self.var(coeff_dict)
                self.uv_vals[j*self.steps + i, :, 0], \
                self.uv_vals[j*self.steps + i, :, 1] = self.var.u, self.var.v
                """plt.figure(figsize=(4,4))
                self.var.plot(cmap = "rainbow")
                plt.scatter(self.var.u, )
                plt.show()
                plt.clf()"""

    def _next_frame(self, i):

        self.points.set_offsets(self.uv_vals[i])

        return self.points,

    def create_anim(self, blit = True):

        self.fig = self.init_frame()
        self.points = plt.scatter([],[], cmap=self.cmap, s=0.1)
        anim_func = self._next_frame
        self.anim = animation.FuncAnimation(self.fig, func = anim_func,
                                            frames = len(self.uv_vals),
                                            repeat = False,
                                            blit = blit, interval = 10)

    def show_anim(self):
        self.create_anim(blit = False)
        plt.show()
        plt.close(self.fig)

    def save_anim(self, filename, fps=60, dpi=400):
        self.create_anim()
        self.anim.save("%s.mp4" %(filename),
                       writer = "ffmpeg", fps = fps,
                       dpi = dpi)
        plt.close(self.fig)


if __name__ == "__main__":
    CG = ChaosGame()
    CG._starting_point()
    CG.iterate(steps=int(1e4))

    test = AnimateVariations(points = [CG.points[:,0], -CG.points[:,1]],
                             color = True, colors = CG._compute_color())
    test.show_anim()
    #test.save_anim("animated/test")
