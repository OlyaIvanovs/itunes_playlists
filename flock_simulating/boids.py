import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

width, height = 640, 480

n = 10
# Random positions clustered within 10-pixel radius around the center
pos = [width/2.0, height/2.0] + 10*np.random.rand(2*n).reshape(n, 2)
# generate array of N random angles in the range [0, 2pi]
angles = 2*math.pi*np.random.rand(n)
# Create arra using the random vector method
vel = np.array(list(zip(np.sin(angles), np.cos(angles))))


class Boids:
    """"""

    def __init__(self):
        """"""
        pass

    def apply_bc(self):
        """Apply boundary conditions"""
        delta = 2.0
        for coord in self.pos:
            if coord[0] > width + delta:
                coord[0] = -delta
            if coord[0] < -delta:
                coord[0] = width + delta
            if coord[1] > height + delta:
                coord[1] = -delta
            if coord[1] < -delta:
                coord[1] = height + delta

    def apply_rules(self):
        """"""
        pass

    def tick(self):
        """"""
        pass


def main():
    """Running the boids simulation"""

    # Set up plot
    fig = plt.figure()
    ax = plt.axes(xlim=(0, width), ylim=(0, height))

    # size and shape of the markers for body
    pts, = ax.plot([], [], markersize=10, c='k', marker='o', ls='None')
    # size and shape of the markers for beak
    beak, = ax.plot([], [], markersize=4, c='r', marker='o', ls='None')
    anim = animation.FuncAnimation(
        fig, tick, fargs=(pts, beak, boids), interval=50)


if __name__ == "__main__":
    main()
