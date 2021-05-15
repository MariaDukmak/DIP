"""Reduce the output of the mapper per text line."""
import sys
import glob
import numpy as np
from const import MATRIX_PATH


def main():
    """
    Read the output of the mapper, and count the results per language.
    """
    counter = np.zeros(len(glob.glob(str(MATRIX_PATH / '*.txt'))), dtype=np.int64)

    for line in sys.stdin:
        # skip white lines
        if len(line) > 1:
            # increase each language with 0-1 for each line
            counter += np.array(line.strip().split('-'), dtype=int)

    sys.stdout.write(f"{'-'.join(map(str, counter))}\n")


if __name__ == '__main__':
    main()
    # our:
    # 126-65
    # hadopy:
    # 131-60
    # target:
    # 119-73
