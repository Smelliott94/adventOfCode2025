# Rolls of paper are @
# Forklift can only get to the paper if < 4 rolls of paper are adjacent (minesweeper number <4)
# initial thought is to load it into a dict where the key is the 2d coordinate and True means that it's a paper roll
# I'm just gonna call papers mines here

# This one I started off by modelling it as a minesweeper-like board with two maps
# one with the boolean if it contains a mine (paper)
# and another with the count of mines in each surrounding cell
# From there it's easy to loop over the first map where the values are True and check if that coordinate has more mines than the threshold


from typing import NamedTuple
from adventofcode2025.day4.input import GRID

example = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@.",
]
example_solved = [
    "..xx.xx@x.",
    "x@@.@.@.@@",
    "@@@@@.x.@@",
    "@.@@@@..@.",
    "x@.@@@@.@x",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "x.@@@.@@@@",
    ".@@@@@@@@.",
    "x.x.@@@.x.",
]

example_answer = 13


class Coord(NamedTuple):
    x: int
    y: int


class Minegrid:
    def __init__(self, grid: list[str]):
        self.grid = grid
        self.grid_map = self.load_grid(self.grid)
        self.number_map = self.assign_numbers(self.grid_map)

    def load_grid(self, grid: list[str]) -> dict[Coord, bool]:
        grid_map: dict[Coord, bool] = {}

        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                grid_map[Coord(i, j)] = True if cell == "@" else False

        return grid_map

    def get_adjacent_mines(self, coordinate: Coord) -> int:
        coordinates_to_check: list[Coord] = []
        adjacent_offset = [-1, 0, 1]
        for i in adjacent_offset:
            for j in adjacent_offset:
                if (i, j) == (0, 0):
                    continue
                coordinates_to_check.append(Coord(coordinate.x + i, coordinate.y + j))
        count = 0

        for coord in coordinates_to_check:
            if self.grid_map.get(coord, False):
                count += 1
        return count

    def assign_numbers(self, grid_map: dict[Coord, bool]) -> dict[Coord, int]:
        return {coord: self.get_adjacent_mines(coord) for coord in grid_map}

    def remove_mine(self, coord: Coord):
        """Decrement mine count in adjacent cells and unmark as a mine in the grid map"""
        self.grid_map[coord] = False
        adjacent_offset = [-1, 0, 1]
        for i in adjacent_offset:
            for j in adjacent_offset:
                if (i, j) == (0, 0):
                    continue
                try:
                    self.number_map[Coord(coord.x + i, coord.y + j)] -= 1
                except KeyError:
                    # Coordinates outside bounds, we don't care
                    pass


def main():
    grid = Minegrid(GRID)
    print(grid.number_map)
    threshold = 4
    answer = 0
    improvable = True
    while improvable:
        last_answer = answer
        coords_to_remove: list[Coord] = []
        for coord, mines in grid.number_map.items():
            if grid.grid_map[coord] and mines < threshold:
                answer += 1
                coords_to_remove.append(coord)

        for coord in coords_to_remove:
            grid.remove_mine(coord)

        if answer == last_answer:
            improvable = False
    print(answer)


if __name__ == "__main__":
    main()
