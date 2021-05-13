"""Reducer file that wil reduce the results of the map function."""
import sys
from itertools import groupby
from operator import itemgetter
from typing import TextIO


def read_mapper_output(input_stream: TextIO, separator='\t') -> str:
    """
    Reads the results of the mapper function.
    :param input_stream: a TextIO object
    :param separator: to split the results
    :return: generator object
    """
    for line in input_stream:
        yield line.rstrip().split(separator, 1)


def main():
    """
    Reads the results of the mapper, and reduce the output of the count.
    """
    data = read_mapper_output(sys.stdin)
    for current_comb, group in groupby(data, itemgetter(0)):
        total = sum(int(count) for _, count in group)
        sys.stdout.write(f"{current_comb}\t{total}\n")


if __name__ == "__main__":
    main()
