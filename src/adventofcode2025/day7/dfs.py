from adventofcode2025.day7.input import TOTALLY_NOT_XMAS_TREE

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


def timelines(grid: list[str]) -> int:
    rows: int = len(grid)
    cols: int = len(grid[0])

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < cols

    # Find source
    start: tuple[int, int] = (0, 0)  # Just to shut pyright up
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
                break

    memo: dict[tuple[int, int], int] = {}
    stack: list[tuple[tuple[int, int], bool]] = [(start, False)]  # (pos, processed flag)

    while stack:
        (r, c), processed = stack.pop()

        # if we got out of bounds, it's the end of the path
        if not in_bounds(r, c):
            memo[(r, c)] = 1
            continue

        if (r, c) in memo:
            continue

        cell = grid[r][c]

        if not processed:  # processed = added children to stack
            # Phase 1: push self again as processed, then children
            stack.append(((r, c), True))

            if cell in ("S", ".", "|"):
                child = (r + 1, c)
                if child not in memo:
                    stack.append((child, False))

            elif cell == "^":
                for child in ((r, c - 1), (r, c + 1)):
                    if child not in memo:
                        stack.append((child, False))

        else:
            # Phase 2: compute using memoized children
            if cell in ("S", ".", "|"):
                child = (r + 1, c)
                memo[(r, c)] = memo[child]

            elif cell == "^":
                left = memo[(r, c - 1)]
                right = memo[(r, c + 1)]
                memo[(r, c)] = left + right

    return memo[start]


def main() -> None:
    print(timelines(grid=TOTALLY_NOT_XMAS_TREE))


if __name__ == "__main__":
    main()
