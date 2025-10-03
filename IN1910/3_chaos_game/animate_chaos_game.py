import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from matplotlib import animation
from chaos_game import ChaosGame


class AnimateChaosGame():
    """
    Class for creating an animation of an n-gon through an ordered sequence of 
    r-values.
    """

    def __init__(self, n = 3, frames = 1000, steps = 100000):

        self.n = n
        self.frames = frames
        self.steps = steps
        self.r_vals = np.linspace(0+1e-6,1-1e-6,frames)
        self.ngon = ChaosGame(n = n)

    def init_frame(self):

        fig = plt.figure(figsize=(9,7))
        plt.axis("equal")
        plt.plot(self.ngon.corners[:,0], self.ngon.corners[:,1], "k--", lw=0.5)
        plt.plot([self.ngon.corners[-1][0], self.ngon.corners[0][0]],
                 [self.ngon.corners[-1][1], self.ngon.corners[0][1]], "k--",
                 lw=0.5)
        plt.scatter(self.ngon.corners[:,0], self.ngon.corners[:,1], c="k")
        plt.tight_layout()

        return fig

    def _next_frame(self, i):

        self.ngon = ChaosGame(n = self.n, r = self.r_vals[i])
        self.ngon._starting_point()
        self.ngon.iterate(steps = self.steps)
        self.points.set_offsets(self.ngon.points)
        self.txt.set_text("r = %.2f"%(self.r_vals[i]))

        return self.points, self.txt,

    def create_anim(self, blit = True):

        self.fig = self.init_frame()
        self.points = plt.scatter([],[], c="black", s=0.1)
        self.txt = plt.text(0.9,1.03,"r=0.00")
        anim_func = self._next_frame
        self.anim = animation.FuncAnimation(self.fig, func = anim_func,
                                            frames = self.frames, repeat = False,
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
    for i in range(3,9):
        test = AnimateChaosGame(n=i)
        test.create_anim()
        test.save_anim("animated/%s-gon" %(i), fps=60, dpi=400)
