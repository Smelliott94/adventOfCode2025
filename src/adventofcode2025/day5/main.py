# fresh or spoiled
# ranges are fresh ingedient ID ranges (inclusive)
# since IDs are available IDs
# first thought it just to scan the ranges and yeet in an entry if an ID is fresh
# since if we build a list then we would have to scan every member until it finds membership
# this took way too long since the ranges are large

# had to do some research on it and if we sort the ranges by their start then we can check possible ranges an id
# can fall into and only check those
# we have to merge the ranges first otherwise we could get some wrong results if there are overlaps
# can use bisect algorithm to find the index where to insert item x in list a

from adventofcode2025.day5.input import ID_INPUT
from typing import NamedTuple
from bisect import bisect_right

example = [
    "3-5",
    "10-14",
    "16-20",
    "12-18",
    "1",
    "5",
    "8",
    "11",
    "17",
    "32",
]


class Range(NamedTuple):
    start: int
    end: int

    def __repr__(self):
        return f"({self.start}-{self.end})"


def load_ranges(input_rows: list[str]) -> tuple[list[Range], list[int]]:
    ranges: list[Range] = []
    id_list: list[int] = []
    for row in input_rows:
        if "-" in row:
            start, end = map(int, row.split("-"))
            ranges.append(Range(start=start, end=end))
        else:
            id_list.append(int(row))
    return ranges, id_list


def merge_ranges(ranges: list[Range]) -> list[Range]:
    ranges.sort()
    merged: list[Range] = []
    for start, end in ranges:
        if merged == []:
            merged.append(Range(start, end))
        last_start, last_end = merged[-1]
        if start <= last_end + 1:
            merged[-1] = Range(last_start, max(last_end, end))
        else:
            merged.append(Range(start, end))
    return merged


def is_fresh(check_id: int, ranges: list[Range]) -> bool:
    range_index = bisect_right([start for start, _ in ranges], check_id) - 1
    if range_index < 0:
        return False
    start, end = ranges[range_index]
    return start <= check_id <= end


def main():
    ranges, id_list = load_ranges(ID_INPUT)
    ranges = merge_ranges(ranges)
    answer = 0
    fresh_ids: list[int] = []

    for i in id_list:
        if is_fresh(i, ranges):
            fresh_ids.append(i)
            answer += 1
    print(answer)
    # second part is just how many ids are valid in the ranges, not what they are, don't have to change anything, can just check
    answer2 = 0
    for range in ranges:
        answer2 += (range.end - range.start) + 1  # inclusive
    print(answer2)


if __name__ == "__main__":
    main()
