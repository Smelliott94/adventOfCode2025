from pathlib import Path

CWD = Path.cwd()


class Dial:
    def __init__(self, start_num=50):
        self.num = start_num
        self.zero_passes = 0

    def wrap_number(self, step: int):
        # Gave up trying to do some floor division stuff for part 2 after getting wrong answer like 5 times
        # just increment tick by tick and count how many times you hit zero
        for _ in range(abs(step)):
            if step > 0:
                self.num = (self.num + 1) % 100

            if step < 0:
                self.num = (self.num - 1) % 100

            if self.num == 0:
                self.zero_passes += 1


def main():
    with open(CWD / "src" / "day1" / "rotation_inputs.txt") as file:
        rotations = [line.strip("\n") for line in file.readlines()]

    dial = Dial(50)
    password = 0
    for rotation in rotations:
        direction = rotation[0]
        step = int(rotation[1:])
        if direction == "R":
            dial.wrap_number(step)
        else:
            dial.wrap_number(-1 * step)

        if dial.num == 0:
            password += 1

    print(f"The easy password is {password}")  # 1135
    print(f"The part 2 password is {dial.zero_passes}")  # 6558


if __name__ == "__main__":
    main()
