# We've got a grid of tiles, some are red
# we want to find the maximum of A = |x1-x2| * |y1-y1|
# it's the largest horizontal distance * largest vertical = rectangle area

# part 2 - The eligible areas are limited by a border which connects the red tiles

from collections import defaultdict

import numpy as np

from adventofcode2025.day9.input import TILES

example = [
    "7,1",
    "11,1",
    "11,7",
    "9,7",
    "9,5",
    "2,5",
    "2,3",
    "7,3",
]


def line_points(src, dest) -> list[tuple[int, int]]:
    (x1, y1), (x2, y2) = src, dest

    if x1 == x2:  # vertical line
        start, end = sorted([y1, y2])
        return [(x1, y) for y in range(start, end + 1)]

    if y1 == y2:  # horizontal line
        start, end = sorted([x1, x2])
        return [(x, y1) for x in range(start, end + 1)]

    raise ValueError("Points are not aligned horizontally or vertically")


def generate_border_points(points: list[tuple[int, int]]) -> set[tuple[int, int]]:
    border_points: list[tuple[int, int]] = []
    for i in range(len(points)):
        for j in range(i, len(points)):
            p1 = points[i]
            p2 = points[j]
            if p1[0] == p2[0] or p1[1] == p2[1]:
                border_points.extend(line_points(src=points[i], dest=points[j]))
    border_points: set[tuple[int, int]] = set(border_points)
    return border_points


# returns dict[y] = list of (left, right) interior spans
def get_interior_spans(border_points):
    rows = defaultdict(list)
    for x, y in border_points:
        rows[y].append(x)

    spans = {}
    for y, xs in rows.items():
        xs.sort()
        it = iter(xs)
        spans[y] = [(left + 1, right - 1) for left, right in zip(it, it)]
    return spans


def is_inside(point: tuple[int, int], spans):
    x, y = point
    if y not in spans:
        return False
    for left, right in spans[y]:
        if left <= x <= right:
            return True
    return False


import matplotlib.pyplot as plt


def plot_points(points):
    # points is a set or list of (x, y) tuples
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    plt.scatter(xs, ys, s=100)  # s controls marker size
    plt.gca().set_aspect("equal")  # keep square grid

    # put gridlines at integer positions
    plt.grid(True, which="both")
    plt.xticks(range(min(xs) - 1, max(xs) + 2))
    plt.yticks(range(min(ys) - 1, max(ys) + 2))

    plt.show(block=False)


def max_area(points: list[tuple[int, int]], n) -> tuple[tuple[int, int], int]:
    # Matrix maths for fun
    points_arr = np.asarray(points)
    X = points_arr[:, 0]
    Y = points_arr[:, 1]

    # we want to find the maximum of A = |x1-x2+1| * |y1-y1+1|

    # pairwise diff matrices with +1 baked in since the tiles have 1 thiccness
    # row matrix - column matrix = n x n matrix because of numpy broadcasting
    # +1 just adds 1 to every element
    dx = np.abs((X[:, None] - X[None, :]) + 1)
    dy = np.abs((Y[:, None] - Y[None, :]) + 1)
    # matrix of areas
    area = dx * dy
    flat = area.ravel()
    sorted_index = np.argsort(flat)
    flat_index = sorted_index[-n]

    i, j = np.unravel_index(flat_index, area.shape)
    i = int(i)
    j = int(j)
    value = area[i, j]
    return (i, j), value


def main():
    points: list[tuple[int, int]] = []
    for row in TILES:
        x, y = row.split(",")
        points.append((int(x), int(y)))
    (i, j), a = max_area(points, 1)
    print(a)
    border_points = generate_border_points(points)
    # plot_points(points)
    # plot_points(border_points)
    all_border_points = border_points.union(set(points))
    # plot_points(all_border_points)
    print(len(all_border_points))
    interior_spans = get_interior_spans(all_border_points)

    # plot_points(safe_points)
    # get the corners of the max area rect
    # get the interior points of the rect
    # check if all of them are in the interior points set
    n = 1
    searching = True
    while searching:
        (i, j), area = max_area(points, n)
        corner1 = points[i]
        corner2 = points[j]
        corner3 = (corner1[0], corner2[1])
        corner4 = (corner2[0], corner1[1])
        rect_border_points = generate_border_points([corner1, corner2, corner3, corner4])
        # plot_points(rect_border_points)
        rect_border_points = rect_border_points.union(set([corner1, corner2, corner3, corner4]))
        # plot_points(safe_points)
        # plot_points(rect_border_points)

        # plot_points(all_touched_points)
        rect_border_points = list(rect_border_points)
        # print(f"Checking {area}")
        for i in range(len(rect_border_points)):
            if not is_inside(rect_border_points[i], interior_spans):
                print(f"not {area}")
                break
            if i == len(rect_border_points) - 1:
                searching = False
                print(f"area is {area}")

        n += 1


# to make it runnably fast I guess replace the border points with spans as well
