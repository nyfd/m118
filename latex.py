import glob
import pandas as pd

# Constants
CE_FILTER_DIR = "ce_filter"


def generate_table(file):
    df = pd.read_csv(file, sep='\t', names=['Path', 'Attr'])
    df['cr'] = df['Attr'] == 'cr'
    df['m'] = df['Attr'] == 'm'
    df['a'] = df['Attr'] == 'a'
    df['c'] = df['Attr'] == 'c'
    df['d'] = df['Attr'] == 'd'

    grouped = df.groupby('Path').sum()\
        .sort_values(['d', 'Path'])\
        .replace(1, '∫') \
        .replace(0, '')

    pd.set_option('display.max_colwidth', None)
    latex_file = open(file + '.latex', 'w')
    latex_file.write(grouped.to_latex(caption=file).replace('∫', '\\faCheck'))
    latex_file.close()

    txt_file = open(file + '.txt', 'w')
    txt_file.write(grouped.to_string().replace('∫', '✓'))
    txt_file.close()


def main():
    files = sorted(glob.glob(f"{CE_FILTER_DIR}/*.ce"))

    for file in files:
        generate_table(file)

    return


if __name__ == '__main__':
    main()
