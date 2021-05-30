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
    """Display the three towers with their disks."""
    # Display the three towers with their disks.
    for level in range(TOTAL_DISKS, -1, -1):
        for tower in (towers["A"], towers["B"], towers["C"]):
            if level >= len(tower):
                display_disk(0)  # Display the bare pole with no disk
            else:
                display_disk(tower[level])
        print()

    # Display the tower labels A, B, C
    empty_space = " " * (TOTAL_DISKS)
    print("{0} A{0}{0} B{0}{0} C\n".format(empty_space))


def display_disk(width):
    """Display disk of the given width."""
    empty_space = " " * (TOTAL_DISKS - width)
    if width == 0:
        center = "||"
    else:
        center = "@"*width + f"_{width}" + "@"*width
    disk = f"{empty_space}{center}{empty_space}"
    print(disk, end="")


def get_player_move(towers):
    """Asks the player for a move. Returns (fromTower, toTower)."""
    while True:
        print('Enter the letters of "from" and "to" towers or QUIT')
        print("(e.g., AB to moves a disk from tower A to tower B.)")
        print()
        response = input("> ").upper().strip()

        if response == 'QUIT':
            print("Thanks for playing!")
            sys.exit()

        if response not in ("AB", "AC", "BA", "BC", "CA", "CB"):
            print("Enter one of AB, AC, BA, BC, CA, CB")
            continue

        from_tower, to_tower = response[0], response[1]
        print(from_tower, to_tower)

        if len(towers[from_tower]) == 0:
            # The "from" tower cannot be an empty tower:
            print("You selected a tower with no disks.")
            continue
        elif len(towers[to_tower]) == 0:
            return from_tower, to_tower
        elif towers[from_tower][-1] > towers[to_tower][-1]:
            print("Can't put larger disks on top of smaller ones.")
            continue
        else:
            return from_tower, to_tower


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
    main()
