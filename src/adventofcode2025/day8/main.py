from collections import defaultdict, deque
from typing import NamedTuple
import heapq

from adventofcode2025.day8.input import COORDINATES


num_of_connections = 1000
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


def merge_connections(pairs: list[tuple[Coordinate, Coordinate]]) -> list[list[Coordinate]]:
    adj: dict[Coordinate, set[Coordinate]] = defaultdict(set)

    for a, b in pairs:
        adj[a].add(b)
        adj[b].add(a)

    visited: set[Coordinate] = set()
    circuits: list[list[Coordinate]] = []

    for node in adj:
        if node in visited:
            continue

        queue = deque([node])
        visited.add(node)
        circuit: list[Coordinate] = []

        while queue:
            cur = queue.popleft()
            circuit.append(cur)
            for nxt in adj[cur]:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        circuits.append(circuit)
    return circuits


def find_closing_pair(
    coordinates: list[Coordinate],
    ordered_pairs: list[tuple[Coordinate, Coordinate]],
) -> tuple[Coordinate, Coordinate] | None:
    """This was all from ChatGPT since i had no idea about graph + cycle detection
    Could have done part 1 this way instead of BFS also
    it's called Union-Find
    """
    # Disjoint-set (union–find) over the coordinates
    parent: dict[Coordinate, Coordinate] = {c: c for c in coordinates}
    comp_count = len(coordinates)

    def find(x: Coordinate) -> Coordinate:
        # path compression
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: Coordinate, b: Coordinate) -> bool:
        nonlocal comp_count
        ra, rb = find(a), find(b)
        if ra == rb:
            return False  # already in same component; no change
        parent[rb] = ra
        comp_count -= 1
        return True

    for a, b in ordered_pairs:
        # only count "real" unions that merge two components
        merged = union(a, b)
        if merged and comp_count == 1:
            # this is the first time everything is in one component
            return (a, b)

    return None  # never became fully connected


def main() -> None:
    input_list: list[str] = COORDINATES
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
        heap.append((distance_squared, (coordA, coordB)))

    heap.sort(key=lambda p: p[0])

    shortest_connections_coords: list[tuple[Coordinate, Coordinate]] = [conn[1] for conn in heap]
    closing_pair = find_closing_pair(coordinates, shortest_connections_coords)
    print("Closing pair:", closing_pair)
    print(closing_pair[0].x * closing_pair[1].x)
    # forms one circuit now since all connections are included
    circuits: list[list[Coordinate]] = merge_connections(shortest_connections_coords)


if __name__ == "__main__":
    main()
