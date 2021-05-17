import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

ON = 255
OFF = 0
vals = [ON, OFF]


def add_glider(i, j, grid):
    """Add a glider with top left cell at (i, j)"""
    glider = np.array([
        [OFF, OFF, ON],
        [ON, OFF, ON],
        [OFF, ON, ON],
    ])
    grid[i:i+3, j:j+3] = glider


def random_grid(n):
    """Returns a grid of n*n random values."""
    return np.random.choice(vals, n*n, p=[0.2, 0.8]).reshape(n, n)


def update(frame_num, img, grid, n):
    """Copy grid since we require 8 neigbors for calculation"""
    new_grid = grid.copy()
    # Go line by line
    for i in range(n):
        for j in range(n):
            # Compute 8 neigbor sum
            total = int((grid[i, (j-1) % n] + grid[i, (j+1) % n] +
                        grid[(i-1) % n, j] + grid[(i+1) % n, j] +
                        grid[(i-1) % n, (j-1) % n] + grid[(i-1) % n, (j+1) % n] +
                        grid[(i+1) % n, (j-1) % n] + grid[(i+1) % n, (j+1) % n])/ON)

            # Apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    new_grid[i, j] = OFF
            else:
                if total == 3:
                    new_grid[i, j] = ON
    # Update data
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img


def main():
    parser = argparse.ArgumentParser(
        description="Runs Conway's Game of Life simulation.")
    # Add arguments
    parser.add_argument('--grid-size', dest='n', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    # start simulatin with glider pattern
    parser.add_argument('--glider', action='store_true', required=False)
    args = parser.parse_args()

    # Set grid size
    n = 100
    if args.n and int(args.n) > 8:
        n = int(args.n)

    # Set animation update interval
    update_interval = 50
    if args.interval:
        update_interval = int(args.interval)

    # Declare grid
    grid = np.array([])
    if args.glider:
        grid = np.zeros(n*n).reshape(n, n)
        add_glider(1, 1, grid)
    else:
        grid = random_grid(n)

    # Set up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation="nearest")
    ani = animation.FuncAnimation(fig, update, fargs=(
        img, grid, n, ), frames=10, interval=update_interval, save_count=50)

    # Save to file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


if __name__ == "__main__":
    """Conway's Game of life simulation."""
    main()
