# Numbers 1-9 in a string
# Find the highest number possible from two batteries
# Can't rearrage
# could iterate from left to right, keeping highest number stored, then we store the 2nd highest number
# if we encounter a higher number than the highest, throw out the two numbers and repeat until end of string
# don't have to account for having the higest number at the end of the string with the input data we have

# for part 2, it's the same logic but we just can't replace the digit it is after the last time it could be checked
# e.g. only replace the 2nd last digit if there is one more digit left, 3rd last digit if there are two more left, and so on
# so if we are looking at a digit, it should not be replaced if n-index_in_digit_str > (battery_len - 1) - i

# can we take the leftmost highest digit, pop that index, and repeat n times?
# loop right to left, store highest digit and index
# we have to also mark the index of the popped number and only look at the slice remaining after it each time

from adventofcode2025.day3.consts import BATTERIES


def highest_two_digits(battery: str) -> str:
    first_digit = 0
    second_digit = 0
    battery_len = len(battery)
    print(f"len is {battery_len}")
    for i, digit in enumerate(battery):
        d = int(digit)
        if d > first_digit and i < battery_len - 1:
            first_digit = d
            second_digit = 0  # we know an answer is wrong then if it ends in 0
            continue
        if d > second_digit:
            second_digit = d

    return str(f"{first_digit}{second_digit}")


def highest_n_digits(battery: str, n: int) -> str:
    """
    wasted like 40 mins on an off-by-one error, had i > n - digit_index in the condition
    i is how far the digit is from the right of the original battery and goes 0-11
    digit_index is the index of the resulting string we're trying to find
    """
    digits = ""
    reversed_battery: list[str] = list(reversed(list(battery)))
    for digit_index in range(n):
        highest_digit: int = 0
        index_to_pop: int = 0
        for i, digit in enumerate(reversed_battery):
            d = int(digit)
            if d >= highest_digit and i >= (n - 1) - digit_index:
                highest_digit = d
                index_to_pop = i
        digits += str(highest_digit)
        reversed_battery = reversed_battery[:index_to_pop]
    print(digits)

    return digits


def main():
    highest_joltage = 0
    for battery in BATTERIES:
        highest_joltage += int(highest_n_digits(battery, 12))
    print(highest_joltage)


if __name__ == "__main__":
    main()
