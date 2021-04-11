import os
import copy
import shutil
import os.path
from os import path

# Constants
ME_DIR = "me"
CE_DIR = "ce"
STATES = ['s2', 's3', 's4', 's5', 's6', 's7', 's8', 's9']


def cleanup(directory):
    if path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


files = dict()


def format_line(file, attr):
    return f"{file}\t{attr}\n"


def read_me_file(file):
    print(f"Processing {file}")
    res = dict()
    with open(file) as fp:
        for line in fp:
            [file, attr, cnt] = line.strip().split("\t")
            tup = (file, attr)
            res[tup] = int(cnt)
    return res


def write_ce_file(file, files):
    with open(file, "w") as fp:
        for (file, attr) in files:
            fp.write(format_line(file, attr))
    return


def subtract(left, right):
    res = copy.deepcopy(left)
    for (file, attr) in right:
        tup = (file, attr)
        if tup in res:
            res[tup] = res[tup] - right[tup]
    clean_dict = {key: val for key, val in res.items() if val > 0 }
    return clean_dict


def filter_dict(dic):
    res = []
    for (file, attr) in dic:
        tup = (file, attr)
        if tup in dic:
            if dic[tup] > 1:
                res.append(tup)
    return sorted(res)


def main():
    cleanup(CE_DIR)

    # Define states
    states = dict((s, dict()) for s in STATES)

    # Load states
    for s in states:
        in_file = f"{ME_DIR}/{s}.me"
        states[s] = read_me_file(in_file)

    # Load noise
    noise = read_me_file(f"{ME_DIR}/noise.me")

    # Compute CE
    for s in states:
        # Subtract noise
        res = subtract(states[s], noise)
        # Subtract other states
        for o in states:
            if s != o:
                res = subtract(res, states[o])

        filtered = filter_dict(res)
        print(f"State {s}: ME = {len(states[s])}, CE = {len(filtered)}")
        out_file = f"{CE_DIR}/{s}.ce"
        write_ce_file(out_file, filtered)

    return


if __name__ == '__main__':
    main()
