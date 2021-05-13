"""reducer."""
import sys
from itertools import groupby
from operator import itemgetter
from typing import TextIO


def read_mapper_output(file_name: TextIO, separator='\t'):
    for line in file_name:
        yield line.rstrip().split(separator, 1)


def main():
    data = read_mapper_output(sys.stdin)
    for current_comb, group in groupby(data, itemgetter(0)):
        total = sum(int(count) for _, count in group)
        sys.stdout.write(f"{current_comb}\t{total}\n")


if __name__ == "__main__":
    main()
