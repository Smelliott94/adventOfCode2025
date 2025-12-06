# Rolls of paper are @
# Forklift can only get to the paper if < 4 rolls of paper are adjacent (minesweeper number <4)
# initial thought is to load it into a dict where the key is the 2d coordinate and True means that it's a paper roll
# I'm just gonna call papers mines here

# This one I started off by modelling it as a minesweeper-like grid with two maps which share keys which are the grid coordinates
# one with the boolean if it contains a mine (paper)
# and another with the count of mines in each surrounding cell
# From there it's easy to loop over either map's keys where there is a mine in one map and more mines than the threshold in the other

# Bonus terminal animation of the paper positions and the most recently removed ones
import sys
import time
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

    def grid_state_as_str_list(
        self, recently_removed_coords: list[Coord] = []
    ) -> list[str]:
        """Go through coordinates
        make a string which has @ if there's a mine or . if there isnt
        chunk the string into the right width
        """
        state_str = ""
        for coord, mine in self.grid_map.items():
            if mine:
                state_str += "@"
            elif coord in recently_removed_coords:
                state_str += "x"
            else:
                state_str += "."
        state: list[str] = []
        width = len(self.grid)  # square
        for row_index in range(len(self.grid)):
            start = row_index * width
            end = start + width
            state.append(state_str[start:end])
        return state


def render(frame: list[str]) -> str:
    return "\n".join(row for row in frame)


def compute_frame_size(frames: list[list[str]]) -> tuple[int, int]:
    max_h = max(len(f) for f in frames)
    max_w = max((len(row) for f in frames for row in f), default=0)
    return max_h, max_w


def normalize_frame(frame: list[str], height: int, width: int) -> list[str]:
    # pad rows to fixed height
    rows = list(frame) + [""] * (height - len(frame))
    # pad / trim columns to fixed width
    return [row.ljust(width)[:width] for row in rows]


def play_ascii_frames(frames: list[list[str]], fps: int = 5):
    delay = 1 / fps

    if not frames:
        return

    height, width = compute_frame_size(frames)

    # Enter alternate screen buffer + hide cursor
    sys.stdout.write("\033[?1049h\033[?25l")
    sys.stdout.flush()

    try:
        for frame in frames:
            fixed = normalize_frame(frame, height, width)

            # Move cursor to top-left, overwrite the whole area
            sys.stdout.write("\033[H")
            sys.stdout.write(render(fixed))
            sys.stdout.flush()

            time.sleep(delay)
    finally:
        # Show cursor again + leave alternate screen buffer
        sys.stdout.write("\033[?25h\033[?1049l")
        sys.stdout.flush()


def main():
    grid = Minegrid(GRID)
    # print(grid.number_map)
    threshold = 4
    answer = 0
    improvable = True
    frames: list[list[str]] = []
    while improvable:
        last_answer = answer
        coords_to_remove: list[Coord] = []
        for coord, mines in grid.number_map.items():
            if grid.grid_map[coord] and mines < threshold:
                answer += 1
                coords_to_remove.append(coord)

        for coord in coords_to_remove:
            grid.remove_mine(coord)

        frames.append(
            grid.grid_state_as_str_list(recently_removed_coords=coords_to_remove)
        )
        if answer == last_answer:
            improvable = False
            frames.append(
                grid.grid_state_as_str_list(recently_removed_coords=coords_to_remove)
            )
    play_ascii_frames(frames)
    print(answer)


if __name__ == "__main__":
    main()
