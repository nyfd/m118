import os
import shutil

# Constants
IDIFF2_PATH = "~/m118/dfxml/python/idifference2.py"
RAW_DIR = "~/m118/avdecrypt"
GE_DIR = "ge"
MAX_RUNS = 3
MAX_STATE = 8


def get_filename(i, s):
    return f"s{s}.{i}"


def get_raw(i, s):
    return f"{RAW_DIR}/{get_filename(i, s)}.raw"


def get_diff(i, s):
    return f"{GE_DIR}/{get_filename(i, s)}.idiff"


def cleanup(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


def main():
    cleanup(GE_DIR)

    for i in range(1, MAX_RUNS + 1):
        print(f"Run {i}, calculating noise {i}")
        os.system(f"python3 {IDIFF2_PATH} {RAW_DIR}/s0.1.raw {RAW_DIR}/noise.{i}.raw  > {GE_DIR}/noise.{i}.idiff")

        for s in range(1, MAX_STATE + 1):
            print(f"Run {i}, step {s}:     comparing s{s} & s{s + 1}")
            os.system(f"python3 {IDIFF2_PATH} {get_raw(i, s)} {get_raw(i, s + 1)} > {get_diff(i, s + 1)}")


if __name__ == '__main__':
    main()

