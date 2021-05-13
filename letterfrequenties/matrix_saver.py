"""Makes a numpy matrix of the map-reduce results."""
import sys
import numpy as np
from const import ACCEPTED_CHARACTERS, SPACE_ALIAS, SPECIAL_CHARACTER_ALIAS, MATRIX_PATH, CHARACTER_SPLITTER

CHARACTERS = ACCEPTED_CHARACTERS.replace(' ', SPACE_ALIAS) + SPECIAL_CHARACTER_ALIAS


def to_matrix(input_stream: str):
    matrix = np.zeros([len(CHARACTERS)] * 2)

    for line in input_stream.split('\n'):
        if '\t' in line:
            comb, count = line.split('\t')
            c1, c2 = comb.split(CHARACTER_SPLITTER)
            matrix[CHARACTERS.index(c1), CHARACTERS.index(c2)] = count

    return matrix / matrix.sum()


def main():
    language = sys.argv[1]
    np.savetxt(MATRIX_PATH / f'{language}.txt', to_matrix(sys.stdin.read()), fmt='%.8f')


if __name__ == '__main__':
    main()
