# have to transpose the matrix to get the expressions out
# it says read right to left one column at a time but multiplication and addition are commutative so
# it doesn't matter what order the expression is in
# didnt bother too much with OOPing this one
# seems the main trick is knowing you can make a matrix and transpose it to get the expressions
from adventofcode2025.day6.input import HOMEWORK
from typing import TypeVar, Sequence
import numpy as np

T = TypeVar("T")

example = [
    "123 328  51 64 ",
    " 45 64  387 23 ",
    "  6 98  215 314",
    "*   +   *   +  ",
]


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


def part1():
    grid: list[list[str]] = []
    for row in HOMEWORK:
        grid.append(row.split())
    print(grid)
    array = np.array(grid)
    expressions = array.transpose()
    calcs: list[str] = []
    for expression in expressions:
        calc = ""
        operator = expression[-1]
        calc = f"{operator}".join(expression)
        calc = calc.strip(operator)
        calcs.append(calc)
    print(calcs)

    answer = 0
    for calc in calcs:
        answer += eval(calc)
    print(answer)


def main():
    grid: list[list[str]] = []
    for row in HOMEWORK:
        grid.append(list(row))
    # array = np.array(grid)
    # array = array.transpose()
    # rewrote to not use numpy and also without the zip trick for my own practice
    array = zip(*grid, strict=True)
    # array = transpose(grid)

    # now the problems are seperated by a row of only whitespace
    # operator is always in the first col
    problems: list[list[str]] = []
    problem: list[str] = []
    operators: list[str] = []
    for row in array:
        if operator := row[-1].strip():
            operators.append(operator)
        row_str = "".join(row)
        if row_str.strip():
            problem.append(row_str.strip(operator))
        else:
            problems.append(problem)
            problem = []
    problems.append(problem)

    calcs: list[str] = []
    for problem, operator in zip(problems, operators):
        calc = ""
        calc = f"{operator}".join(problem)
        calc = calc.strip(operator)
        calcs.append(calc)

    answer = 0
    for calc in calcs:
        answer += eval(calc.replace(" ", ""))
    print(answer)


if __name__ == "__main__":
    main()
