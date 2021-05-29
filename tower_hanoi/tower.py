"""
Move the tower of disks, one disk at a time, to another tower. Larger
disks cannot rest on top of a smaller disk.

1. The player can move only one disk at a time.
2. The player can only move disks to and from the top of a tower.
3. The player can never place a larger disk on top of a smaller disk.

This program presents the puzzle to a human player to solve.
"""

import copy
import sys

TOTAL_DISKS = 5

# Start with all disks on tower A:
SOLVED_TOWER = list(range(TOTAL_DISKS, 0, -1))


def display_towers(towers):
    """"""
    pass


def display_disk(width):
    """Display disk of the given width."""
    empty_space = " " * (TOTAL_DISKS - width)
    if width == 0:
        center = "||"
    else:
        center = "@"*width + f"_{width}" + "@"*width
    disk = f"{empty_space}{center}{empty_space}"
    print(disk)


def get_player_move():
    """"""
    pass


def main():
    """Runs a single game of the Tower of Hanoi."""
    print("Move the tower of disks, one disk at a time, to another tower. Larger disks cannot rest on top of a smaller disk.")

    towers = {"A": copy.copy(SOLVED_TOWER), "B": [], "C": []}

    while True:
        # Display towers and disks
        display_towers(towers)

        # Ask player to move a disk
        from_tower, to_tower = get_player_move(towers)

        # Move disks
        disk = towers[from_tower].pop()
        towers[to_tower].append(disk)

        # Check if puzzle solved is.
        if SOLVED_TOWER in (towers["B"], towers["C"]):
            display_towers(towers)
            print("You have solved th puzzle!")
            sys.exit()


if __name__ == "__main__":
    # main()
    for i in range(6):
        display_disk(i)
