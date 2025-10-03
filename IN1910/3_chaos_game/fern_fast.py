import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from numba import jitclass
from numba import float64
from numba.typed import Dict

import time

spec = [('a', float64), ('b', float64), ('c', float64),
        ('d', float64), ('e', float64), ('f', float64),
        ('x', float64), ('y', float64)]

@jitclass(spec)
class AffineTransform_fast():

    def __init__(self, a=0, b=0, c=0, d=0, e=0, f=0):

        self.a, self.b, self.c, self.d, self.e, self.f = a, b, c, d, e, f

    def call(self, point=[0,0]):

        x = self.a*point[0] + self.b*point[1] + self.e
        y = self.c*point[0] + self.d*point[1] + self.f

        return [x, y]


class Fern_fast():

    def __init__(self, f_1, f_2, f_3, f_4, p_vals):

        assert sum(p_vals) == 1, "Probability sum not 1"
        self.f1 = AffineTransform_fast(f_1[0],f_1[1],f_1[2],f_1[3],f_1[4],f_1[5])
        self.f2 = AffineTransform_fast(f_2[0],f_2[1],f_2[2],f_2[3],f_2[4],f_2[5])
        self.f3 = AffineTransform_fast(f_3[0],f_3[1],f_3[2],f_3[3],f_3[4],f_3[5])
        self.f4 = AffineTransform_fast(f_4[0],f_4[1],f_4[2],f_4[3],f_4[4],f_4[5])
        self.p_cumulative = np.asarray([p_vals[0], sum(p_vals[0:2]),
                                       sum(p_vals[0:3]), sum(p_vals)])

    def iterate(self, steps=50000, p0=[0,0]):

        self.points = np.zeros((steps,2), dtype=np.float64)
        self.points[0] = p0
        self.r = np.random.random(steps)

        points = iterate_fast(self.points, steps, self.r,
                              self.f1, self.f2, self.f3, self.f4,
                              self.p_cumulative)


@jit(cache=True, nopython=True)
def iterate_fast(points, steps, r, f1, f2, f3, f4, p_cumulative):
    for i in range(1, steps):
        if r[i] < p_cumulative[0]:
            points[i] = f1.call(points[i-1])
        elif r[i] < p_cumulative[1]:
            points[i] = f2.call(points[i-1])
        elif r[i] < p_cumulative[2]:
            points[i] = f3.call(points[i-1])
        elif r[i] < p_cumulative[3]:
            points[i] = f4.call(points[i-1])

    return points


if __name__=="__main__":

    f_1 = [0, 0, 0, 0.16, 0, 0]
    f_2 = [0.85, 0.04, -0.04, 0.85, 0, 1.60]
    f_3 = [0.20, -0.26, 0.23, 0.22, 0, 1.60]
    f_4 = [-0.15, 0.28, 0.26, 0.24, 0, 0.44]
    p_vals = [0.01, 0.85, 0.07, 0.07]

    fern = Fern_fast(f_1, f_2, f_3, f_4, p_vals)
    t0 = time.time()
    fern.iterate(steps=int(1e6))
    t1 = time.time()
    print(t1-t0)
