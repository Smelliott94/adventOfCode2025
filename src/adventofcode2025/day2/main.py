# first half
# Invalid is a sequence of digits repeated twice
# odd len can't be invalid

# second half
# Invalid is a sequence of any length repeated more than once
DATA = [
    "24-46",
    "124420-259708",
    "584447-720297",
    "51051-105889",
    "6868562486-6868811237",
    "55-116",
    "895924-1049139",
    "307156-347325",
    "372342678-372437056",
    "1791-5048",
    "3172595555-3172666604",
    "866800081-866923262",
    "5446793-5524858",
    "6077-10442",
    "419-818",
    "57540345-57638189",
    "2143479-2274980",
    "683602048-683810921",
    "966-1697",
    "56537997-56591017",
    "1084127-1135835",
    "1-14",
    "2318887654-2318959425",
    "1919154462-1919225485",
    "351261-558210",
    "769193-807148",
    "4355566991-4355749498",
    "809094-894510",
    "11116-39985",
    "9898980197-9898998927",
    "99828221-99856128",
    "9706624-9874989",
    "119-335",
]


def split_evenly(num: str, n: int) -> list[str]:
    size = len(num) // n
    return [num[i * size : (i + 1) * size] for i in range(n)]


def get_range(range_str: str) -> list[int]:
    start, end = range_str.split("-")
    return list(range(int(start), int(end) + 1))


def is_invalid(n: int) -> bool:
    ns = str(n)
    n_len = len(ns)
    if n_len == 1:  # can't be valid if there's nothing to repeat
        return False

    for num_of_chunks in range(2, n_len + 1):
        if (
            not (n_len % num_of_chunks) == 0
        ):  # can't be a repeating pattern if it doesn't have same length
            continue
        chunks = split_evenly(ns, num_of_chunks)
        if len(set(chunks)) == 1:
            return True
    return False


def main():
    invalid_ids: list[int] = []
    for rangestr in DATA:
        for number in get_range(
            rangestr
        ):  # get the range of numbers indicated by the string
            if is_invalid(number):
                invalid_ids.append(number)
    print(sum(invalid_ids))


if __name__ == "__main__":
    main()
