import sys
import time


def render(frame: list[str]) -> str:
    return "\n".join(row for row in frame)


def compute_frame_size(frames: list[list[str]]) -> tuple[int, int]:
    max_h = max(len(f) for f in frames)
    max_w = max((len(row) for f in frames for row in f), default=0)
    return max_h, max_w


def normalize_frame(frame: list[str], height: int, width: int) -> list[str]:
    # pad rows to fixed height
    rows = list(frame) + [""] * (height - len(frame))
    # pad / trim columns to fixed width
    return [row.ljust(width)[:width] for row in rows]


def play_ascii_frames(frames: list[list[str]], fps: int = 5):
    delay = 1 / fps

    if not frames:
        return

    height, width = compute_frame_size(frames)

    # Enter alternate screen buffer + hide cursor
    sys.stdout.write("\033[?1049h\033[?25l")
    sys.stdout.flush()

    try:
        for frame in frames:
            fixed = normalize_frame(frame, height, width)

            # Move cursor to top-left, overwrite the whole area
            sys.stdout.write("\033[H")
            sys.stdout.write(render(fixed))
            sys.stdout.flush()

            time.sleep(delay)
    finally:
        # Show cursor again + leave alternate screen buffer
        sys.stdout.write("\033[?25h\033[?1049l")
        sys.stdout.flush()
