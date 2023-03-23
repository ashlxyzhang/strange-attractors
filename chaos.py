import random
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import math
from time import time
import numpy as np

n = 10
found = 0

def update(i):
    # Randomly choose 75% of the points to change size
    indices = np.random.choice(10000, int(0.01*10000), replace=False)
    scat.set_sizes([1.5 if j in indices else 0.2 for j in range(10000)])
    return scat,

while found < n:

    converging = False
    lyapunov = 0

    # starting point
    x = random.uniform(-0.5, 0.5)
    y = random.uniform(-0.5, 0.5)

    # random alternative point
    xe = x + random.uniform(-0.5, 0.5) / 1000
    ye = y + random.uniform(-0.5, 0.5) / 1000

    # distance
    dx = xe - x
    dy = ye - y
    d0 = math.sqrt(dx * dx + dy * dy)

    # random parameter vector
    a = [random.uniform(-2, 2) for i in range(12)]

    # store path
    x_list = [x]
    y_list = [y]

    for i in range(10000):

        # compute next point using quadratic map
        xn = a[0] + a[1] * x + a[2] * x * x + a[3] * y + a[4] * y * y + a[5] * x * y
        yn = a[6] + a[7] * x + a[8] * x * x + a[9] * y + a[10] * y * y + a[11] * x * y

        # check if converge to infinity
        if xn > 1e10 or yn > 1e10 or xn < -1e10 or yn < -1e10:
            converging = True
            break

        # check if converge to point
        if abs(x - xn) < 1e-10 and abs(y - yn) < 1e-10:
            converging = True
            break

        # check for chaotic behavior
        if i > 1000:

            # compute next alt point
            xen = a[0] + a[1] * xe + a[2] * xe * xe + a[3] * ye + a[4] * ye * ye + a[5] * xe * ye
            yen = a[6] + a[7] * xe + a[8] * xe * xe + a[9] * ye + a[10] * ye * ye + a[11] * xe * ye

            # distance btwn new points
            dx = xen - xn
            dy = yen - yn
            d = math.sqrt(dx * dx + dy * dy)

            # lyapunov exponent
            lyapunov += math.log(abs(d/d0))

            # rescale alt point
            xe = xn + d0*dx/d
            ye = yn + d0*dy/d

        # update (x, y)
        x = xn
        y = yn

        # store in path list
        x_list.append(x)
        y_list.append(y)

    if not converging and lyapunov >= 500:
        found += 1

        print("Starting point: (" + str(x) + ", " + str(y) + ")")
        print("Parameter vector: " + str(a))

        # clear plot
        # plt.clf()
        plt.style.use("dark_background")

        fig = plt.figure()

        plt.axis("off")
        scat = plt.scatter(x_list[100:], y_list[100:], s = 0.2, alpha=0.8, c = "white", linewidths=0)

        ani = FuncAnimation(fig, update, frames=20, interval=100)
        writer = PillowWriter(fps = 10)
        ani.save("exhibits/" + str(time()) + ".gif", writer)

