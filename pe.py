import glob
import os
import re
import shutil
import os.path
from os import path

# Constants
GE_DIR = "ge"
PE_DIR = "pe"

NEW_FILES = "New files:"
DELETED_FILES = "Deleted files:"
RENAMED_FILES = "Renamed files:"
MODIFIED_FILES = "Files with modified contents:"
CHANGED_PROPERTIES_FILES = "Files with changed properties:"


def cleanup(directory):
    if path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


new_files = dict()
deleted_files = dict()
renamed_files = dict()
modified_files = dict()


def parse1(line):
    m = re.match(r".+\t(.+)\t.+", line)
    if m:
        return m.group(1)
    return None


def parse2(line):
    m = re.match(r"(.+)\t(.+)time changed,.+", line)
    if m:
        return m.group(1), m.group(2)
    return None, None


def process_new_files_line(line):
    file = parse1(line)
    if file:
        new_files[file] = ["m", "a", "c", "cr"]
    return


def process_deleted_files_line(line):
    file = parse1(line)
    if file:
        deleted_files[file] = ["d"]
    return


def process_renamed_files_line(line):
    file, attr = parse2(line)
    if file and attr:
        renamed_files.setdefault(file, []).append(attr)
    return


def process_modified_files_line(line):
    file, attr = parse2(line)
    if file and attr:
        modified_files.setdefault(file, []).append(attr)
    return


def format_line(file, stempel):
    return f"{file}\t{stempel}\n"


def read_idiff_file(file):
    new_files.clear()
    deleted_files.clear()
    renamed_files.clear()
    modified_files.clear()

    with open(file) as fp:
        for next_section in [NEW_FILES, DELETED_FILES, RENAMED_FILES,
                             MODIFIED_FILES, CHANGED_PROPERTIES_FILES]:
            for line in iter(lambda: fp.readline().rstrip(), next_section):
                if next_section == NEW_FILES:
                    pass
                elif next_section == DELETED_FILES:
                    process_new_files_line(line)
                elif next_section == RENAMED_FILES:
                    process_deleted_files_line(line)
                elif next_section == MODIFIED_FILES:
                    process_renamed_files_line(line)
                elif next_section == CHANGED_PROPERTIES_FILES:
                    process_modified_files_line(line)
    return


def write_pe_file(file):
    with open(file, "w") as fp:
        for dic in [new_files, deleted_files, renamed_files, modified_files]:
            for file in dic:
                for attr in dic[file]:
                    fp.write(format_line(file, attr))
    return


def main():
    cleanup(PE_DIR)

    files = sorted(glob.glob(f"{GE_DIR}/*.idiff"))

    for in_file in files:
        out_file = in_file.replace(GE_DIR, PE_DIR).replace(".idiff", ".pe")

        print(f"Processing {in_file} -> {out_file}")
        read_idiff_file(in_file)
        write_pe_file(out_file)

        print(f"\tNew:\t\t{len(new_files)}")
        print(f"\tDeleted:\t{len(deleted_files)}")
        print(f"\tRenamed:\t{len(renamed_files)}")
        print(f"\tModified:\t{len(modified_files)}")
    return


if __name__ == '__main__':
    main()
