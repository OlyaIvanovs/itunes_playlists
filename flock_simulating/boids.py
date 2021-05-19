import math
import numpy as np
from scipy.spatial.distance import squareform, pdist, cdist
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
from numpy.linalg import norm

width, height = 640, 480


class Boids:
    """"""

    def __init__(self, n):
        """Initialize the boid simulation."""
        # Initial position and velocities
        # Random positions clustered within 10-pixel radius around the center
        self.pos = [width/2.0, height/2.0] + \
            10*np.random.rand(2*n).reshape(n, 2)
        # generate array of N random angles in the range [0, 2pi]
        angles = 2*math.pi*np.random.rand(n)
        # Create arra using the random vector method
        self.vel = np.array(list(zip(np.sin(angles), np.cos(angles))))
        self.n = n
        # Maximum magnitude of velocities calculated by rules
        self.max_rule_vel = 0.03
        # Maximum magnitude of the final velocity
        self.max_vel = 2.0

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

    def _apply_rules(self):
        """Apply the three core rules: Separation, Alignment, Cohesion"""
        # Separation: keep min distance between the boids
        D = self.dist_matrix() < 25.0
        vel = self.pos*D.sum(axis=1).reshape(self.n, 1) - D.dot(self.pos)
        self.limit

    def button_press(self, event):
        """Event handler if mouse button is pressed"""
        # Left click to add a boid
        if event.button is 1:
            self.pos = np.concatenate(
                (self.pos, np.array([[event.xdata, event.ydata]])), axis=0)
            # Generate a random velocity
            angles = 2*math.pi*np.random.rand(1)
            vel = np.array(list(zip(np.sin(angles), np.cos(angles))))
            self.vel = np.concatenate((self.vel, vel), axis=0)
            self.n += 1  # increment the count of boids
        # Right click to scatter boids
        elif event.button is 3:
            # Add scattering velocity
            self.vel += 0.1*(self.pos - np.array([[event.xdata, event.ydata]]))

    def tick(self):
        """Update the simulation by one time step."""
        # Get pairwise distance
        self.dist_matrix = squareform(pdist(self.pos))
        # Apply rules
        self.vel += self._apply_rules()

    def limit_vec(self, vec, max_val):
        """Limit the magnitude of the 2D vector."""
        mag = norm(vec)
        if mag > max_val:
            vec[0], vec[1] = vec[0]*max_val/mag, vec[1]*max_val/mag

    def limit(self, vecs, max_val):
        """Limit the magnitude of 2D vectors in array."""
        for vec in vecs:
            self.limit_vec(vec, max_val)


def tick(frame_num, pts, beak, boids):
    """Called at each time step to update the animation."""
    boids.tick(frame_num, pts, beak)
    return pts, beak


def main():
    """Running the boids simulation"""
    print("starting boids...")

    parser = argparse.ArgumentParser(
        description="Implementing Craig Reynolds Bpid...")
    parser.add_argument('num_boids', dest='n', required=False)
    args = parser.parse_args()

    # Set the initial number of boids
    n = 100
    if args.n:
        n = int(args.n)

    # Create boids
    boids = Boids(n)

    # Set up plot
    fig = plt.figure()
    ax = plt.axes(xlim=(0, width), ylim=(0, height))

    # size and shape of the markers for body
    pts, = ax.plot([], [], markersize=10, c='k', marker='o', ls='None')
    # size and shape of the markers for beak
    beak, = ax.plot([], [], markersize=4, c='r', marker='o', ls='None')
    anim = animation.FuncAnimation(
        fig, tick, fargs=(pts, beak, boids), interval=50)

    # Add a 'button_press' event handler
    cid = fig.canvas.mpl_connect(
        'button_press_event', boids.button_press)  # mouse button is pressed

    plt.show()


if __name__ == "__main__":
    main()
