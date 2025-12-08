from collections import Counter
from typing import NamedTuple
import heapq


example: list[str] = [
    "162,817,812",
    "57,618,57",
    "906,360,560",
    "592,479,940",
    "352,342,300",
    "466,668,158",
    "542,29,236",
    "431,825,988",
    "739,650,466",
    "52,470,668",
    "216,146,977",
    "819,987,18",
    "117,168,530",
    "805,96,715",
    "346,949,466",
    "970,615,88",
    "941,993,340",
    "862,61,35",
    "984,92,344",
    "425,690,689",
]


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int


# map of coordinates that have a connection
circuits: dict[Coordinate, set[Coordinate]] = {}


def main() -> None:
    input_list: list[str] = example
    num_of_connections = 10
    coordinates: list[Coordinate] = [Coordinate(*[int(i) for i in row.split(",")]) for row in input_list]

    # every coordinate combo
    all_coord_pairs: list[tuple[Coordinate, Coordinate]] = [
        (coordinates[i], coordinates[j]) for i in range(len(coordinates)) for j in range(i + 1, len(coordinates))
    ]
    # formula for dist between 2 points is sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)
    # we don't need to know the actual distance, just the n closest boxes, so we dont need to sqrt all of them
    heap: list[tuple[int, tuple[Coordinate, Coordinate]]] = []
    for coordA, coordB in all_coord_pairs:
        distance_squared = ((coordB.x - coordA.x) ** 2) + ((coordB.y - coordA.y) ** 2) + ((coordB.z - coordA.z) ** 2)
        # want to replace largest item so negate distance so heap[0] is the largest distance in the heap
        if len(heap) < num_of_connections:
            heapq.heappush(heap, (-distance_squared, (coordA, coordB)))
        else:
            if distance_squared < -heap[0][0]:
                _ = heapq.heapreplace(heap, (-distance_squared, (coordA, coordB)))

    shortest_connections: list[tuple[int, tuple[Coordinate, Coordinate]]] = heapq.nsmallest(num_of_connections, heap, key=lambda p: -p[0])
    all_connected_points: list[Coordinate] = []
    for _, conn in shortest_connections:
        for point in conn:
            all_connected_points.append(point)

    print(Counter(all_connected_points))


if __name__ == "__main__":
    main()
