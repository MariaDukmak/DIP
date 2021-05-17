"""Prints the results of the reducer."""
import sys
import glob
import os
from const import MATRIX_PATH


def main():
    """
    Print the results of the reducer reading the output of it.
    """
    languages = [os.path.basename(path)[:-4] for path in glob.glob(str(MATRIX_PATH / '*.txt'))]
    counts = sys.stdin.read().split('\n')[0].split('-')
    for language, count in zip(languages, counts):
        print(f"{language}\t{count}")


if __name__ == '__main__':
    main()
