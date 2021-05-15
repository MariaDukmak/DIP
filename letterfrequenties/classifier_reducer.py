import sys
import glob
import numpy as np
from const import MATRIX_PATH


def main():

    counter = np.zeros(len(glob.glob(str(MATRIX_PATH / '*.txt'))), dtype=np.int64)

    for line in sys.stdin:
        if len(line) > 1:
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
