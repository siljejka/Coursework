import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from numba import jitclass
from numba import float64
from numba.typed import Dict
import statistics as st

import time
from fern import AffineTransform, Fern
from fern_fast import AffineTransform_fast, Fern_fast, iterate_fast

import multiprocessing as mp #check if we can multiprocess this

def compare_speed(return_val = False):

    f_1 = [0, 0, 0, 0.16, 0, 0]
    f_2 = [0.85, 0.04, -0.04, 0.85, 0, 1.60]
    f_3 = [0.20, -0.26, 0.23, 0.22, 0, 1.60]
    f_4 = [-0.15, 0.28, 0.26, 0.24, 0, 0.44]
    func_vals = [f_1, f_2, f_3, f_4]
    p_vals = [0.01, 0.85, 0.07, 0.07]

    steps = [int(1e4), int(5e4), int(1e5), int(5e5), int(1e6), int(5e6), int(1e7), int(5e7)]
    fern1 = Fern(func_vals, p_vals)
    fern2 = Fern_fast(f_1, f_2, f_3, f_4, p_vals)

    times = []

    #initialise all underlying functions, for fair function to function comparison
    fern1.iterate(steps=10)
    fern2.iterate(steps=10)

    for n in steps:
        t0 = time.time()
        fern1.iterate(steps=n)
        t1 = time.time()
        fern2.iterate(steps=n)
        t2 = time.time()

        slow = t1-t0
        fast = t2-t1

        times.append([n, slow, fast])


    if return_val == True:
        return times

    else:
        txt = " %10s| %10s| %10s| %10s\n"%("n","slow","fast","(slow/fast)")
        for i in range(len(times)):
            txt += "%10.1e |"%(times[i][0])
            txt += "%10.6s |"%(times[i][1])
            txt += "%10.6s |"%(times[i][2])
            txt += "%10.6s "%(times[i][3])
            txt += "\n"
        print(txt)

        outfile = open("time_comparison.txt", "w")
        outfile.write(txt)
        outfile.close()

def compare_speed_median():

    f_1 = [0, 0, 0, 0.16, 0, 0]
    f_2 = [0.85, 0.04, -0.04, 0.85, 0, 1.60]
    f_3 = [0.20, -0.26, 0.23, 0.22, 0, 1.60]
    f_4 = [-0.15, 0.28, 0.26, 0.24, 0, 0.44]
    func_vals = [f_1, f_2, f_3, f_4]
    p_vals = [0.01, 0.85, 0.07, 0.07]

    steps = [int(1e4), int(1e5), int(1e6), int(5e6), int(1e7)]
    fern1 = Fern(func_vals, p_vals)
    fern2 = Fern_fast(f_1, f_2, f_3, f_4, p_vals)

    times = []

    #initialise all underlying functions, for fair function to function comparison
    fern1.iterate(steps=10)
    fern2.iterate(steps=10)

    times = []

    for n in steps:
        slow_times = []
        fast_times = []
        for i in range(10):
            t0 = time.time()
            fern1.iterate(steps=n)
            t1 = time.time()
            fern2.iterate(steps=n)
            t2 = time.time()

            slow_times.append(t1-t0)
            fast_times.append(t2-t1)

        slow = st.median(slow_times)
        fast = st.median(fast_times)
        times.append([n, slow, fast, (slow/fast)])

    txt = " %10s| %10s| %10s| %10s\n"%("n","slow","fast","(slow/fast)")
    for i in range(len(times)):
        txt += "%10.1e |"%(times[i][0])
        txt += "%10.6s |"%(times[i][1])
        txt += "%10.6s |"%(times[i][2])
        txt += "%10.6s "%(times[i][3])
        txt += "\n"

    print(txt)


def compare_speed_median_mp(N):

    times = []
    pool_arguments = [True for i in range(N)]
    pool = mp.Pool(processes = mp.cpu_count()-4)
    results = pool.map(compare_speed, pool_arguments)
    pool.close()

    print("MP done")

    slow_times = [[] for i in range(len(results[0]))]
    fast_times = [[] for i in range(len(results[0]))]
    n_vals = [[] for i in range(len(results[0]))]
    for i in range(len(results[0])):
        n_vals[i].append(results[0][i][0])

    for i in range(len(results)):
        for j in range(len(results[i])):
            slow_times[j].append(results[i][j][1])
            fast_times[j].append(results[i][j][2])


    for i in range(len(n_vals)):
        n_vals[i].append(st.median(slow_times[i]))
        n_vals[i].append(st.median(fast_times[i]))
        n_vals[i].append(st.median(slow_times[i])/st.median(fast_times[i]))


    txt = " %10s| %10s| %10s| %10s\n"%("n","slow","fast","(slow/fast)")
    for i in range(len(n_vals)):
        txt += "%10.1e |"%(n_vals[i][0])
        txt += "%10.6s |"%(n_vals[i][1])
        txt += "%10.6s |"%(n_vals[i][2])
        txt += "%10.6s "%(n_vals[i][3])
        txt += "\n"

    print(txt)

    outfile = open("time_comparison.txt", "w")
    outfile.write(txt)
    outfile.close()

if __name__=="__main__":
    #compare_speed(0)
    #compare_speed_median()
    compare_speed_median_mp(20)
