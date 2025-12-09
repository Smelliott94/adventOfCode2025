# We've got a grid of tiles, some are red
# we want to find the maximum of A = |x1-x2| * |y1-y1|
# it's the largest horizontal distance * largest vertical = rectangle area
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


points: list[tuple[int, int]] = []
for row in example:
    x, y = row.split(",")
    points.append((int(x), int(y)))

# Matrix maths for fun
points_arr = np.asarray(points)
X = points_arr[:, 0]
Y = points_arr[:, 1]

# we want to find the maximum of A = |x1-x2+1| * |y1-y1+1|

# pairwise diff matrices with +1 baked in since the tiles have 1 thiccness
# row matrix - column matrix = n x n matrix
dx = np.abs((X[:, None] - X[None, :]) + 1)
dy = np.abs((Y[:, None] - Y[None, :]) + 1)
print(dx)
print(dy)
# matrix of areas
area = dx * dy
print(area)
# check what the max value in the matrix is
flat_index = np.argmax(area)
i, j = np.unravel_index(flat_index, area.shape)
print(area[i, j])
