# How many times will the beam be split?
# the beam splits if there's a '^' under it
# splitting means the beam starts to the left and right of the '^'
# try making a node class which keeps track of state

# in part 2, instead of editing the registry in place when a splitter is hit, it splits the timeline
# we can go left on the exiting registry, then create a copy of the registry which goes right from that point

from typing import Literal, TypeAlias, override
from adventofcode2025.day7.input import TOTALLY_NOT_XMAS_TREE

ValidIdChar: TypeAlias = Literal["S", ".", "^", "|"]
VALID_ID_CHARS: list[ValidIdChar] = ["S", ".", "^", "|"]

node_type_map: dict[ValidIdChar, str] = {
    "S": "Source",
    ".": "Empty",
    "^": "Splitter",
    "|": "Beam",
}


class Node:
    total_splits: int = 0

    def __init__(self, x: int, y: int, id_char: ValidIdChar) -> None:
        self.x: int = x
        self.y: int = y
        self.id_char: ValidIdChar = id_char
        self.source: bool = id_char == "S"
        self.beam: bool = id_char == "|"
        self.splitter: bool = id_char == "^"
        self.empty: bool = id_char == "."
        node_registry[(self.x, self.y)] = self

    def right(self) -> "Node":
        return node_registry[(self.x, self.y + 1)]

    def left(self) -> "Node":
        return node_registry[(self.x, self.y - 1)]

    def above(self) -> "Node":
        return node_registry[(self.x - 1, self.y)]

    def below(self) -> "Node":
        return node_registry[(self.x + 1, self.y)]

    @override
    def __repr__(self):
        return f"Node({self.x}, {self.y} | {node_type_map[self.id_char]})"

    def make_beam(self) -> None:
        self.beam = True
        self.splitter = False
        self.empty = False
        self.id_char = "|"

    def splitter_hit(self) -> None:
        Node.total_splits += 1


NodeRegistry: TypeAlias = dict[tuple[int, int], Node]
node_registry: NodeRegistry = {}

example: list[str] = [
    ".......S.......",
    "...............",
    ".......^.......",
    "...............",
    "......^.^......",
    "...............",
    ".....^.^.^.....",
    "...............",
    "....^.^...^....",
    "...............",
    "...^.^...^.^...",
    "...............",
    "..^...^.....^..",
    "...............",
    ".^.^.^.^.^...^.",
    "...............",
]


def main() -> None:
    input_src: list[str] = TOTALLY_NOT_XMAS_TREE
    for i, row in enumerate(input_src):
        for j, cell in enumerate(row):
            assert cell in VALID_ID_CHARS
            _ = Node(x=i, y=j, id_char=cell)

    for i, row in enumerate(input_src):
        for j, cell in enumerate(row):
            node: Node = node_registry[(i, j)]
            if node.source:
                node.below().make_beam()

            if node.x == 0:
                continue

            if node.splitter and node.above().beam:
                node.splitter_hit()
                node.left().make_beam()
                node.right().make_beam()

            if node.empty and node.above().beam:
                node.make_beam()

    print(Node.total_splits)


if __name__ == "__main__":
    main()
