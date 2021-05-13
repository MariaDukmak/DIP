"""reducer."""
import sys
from itertools import groupby
from operator import itemgetter


def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)


def main():
    data = read_mapper_output(sys.stdin)
    for current_word, group in groupby(data, itemgetter(0)):
        total = sum(int(count) for current_word, count in group)
        sys.stdout.write(f"{current_word}\t{total}\n")


if __name__ == "__main__":
    main()
