from typing import TypeVar, Sequence

T = TypeVar("T")


def transpose(matrix: Sequence[Sequence[T]]) -> list[list[T]]:
    if not matrix:
        return []
    rows = len(matrix)
    cols = len(matrix[0])

    transposed: list[list[T]] = [[] for _ in range(cols)]
    for row in range(rows):
        for col in range(cols):
            transposed[col].append(matrix[row][col])
    return transposed
