import os
import shutil
import os.path
from os import path

# Constants
PE_DIR = "pe"
ME_DIR = "me"
STATES = ['noise', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9']


def cleanup(directory):
    if path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


files = dict()


def format_line(tup, cnt):
    file, attr = tup
    return f"{file}\t{attr}\t{cnt}\n"


def read_pe_file(file):
    print(f"Processing {file}")
    with open(file) as fp:
        for line in fp:
            [file, attr] = line.strip().split("\t")
            tup = (file, attr)
            val = files.setdefault(tup, 0)
            files[tup] = val + 1
    return


def write_me_file(file):
    with open(file, "w") as fp:
        for tup in sorted(files):
            fp.write(format_line(tup, files[tup]))
    return


def main():
    cleanup(ME_DIR)

    for state in STATES:
        files.clear()

        for i in [1, 2, 3]:
            in_file = f"{PE_DIR}/{state}.{i}.pe"
            read_pe_file(in_file)

        out_file = f"{ME_DIR}/{state}.me"
        write_me_file(out_file)

    return


if __name__ == '__main__':
    main()
