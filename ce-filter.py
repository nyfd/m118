import glob
import os
import shutil
import os.path
from os import path

# Constants
CE_DIR = "ce"
CE_FILTER_DIR = "ce_filter"


def cleanup(directory):
    if path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


def main():
    cleanup(CE_FILTER_DIR)

    ce_files = sorted(glob.glob(f"{CE_DIR}/*.ce"))

    for file in ce_files:
        out_file = file.replace(f"{CE_DIR}/", f"{CE_FILTER_DIR}/")
        os.system(f"grep -i 'com\.axa\.trx\.' {file} > {out_file}")

    return


if __name__ == '__main__':
    main()
