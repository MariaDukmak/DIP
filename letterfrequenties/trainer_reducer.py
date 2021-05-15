"""Reducer file that wil reduce the results of the map function."""
import sys
from itertools import groupby


def main():
    """
    Reads the results of the mapper, and reduce the output of the count.
    """
    data = [line.rstrip().split('\t') for line in sys.stdin]
    for current_comb, group in groupby(data, lambda i: i[0]):
        sys.stdout.write(f"{current_comb}\t{len(list(group))}\n")


if __name__ == "__main__":
    main()