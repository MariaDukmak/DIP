import sys
import numpy as np

characters = 'abcdefghijklmnopqrstuwxyz_!'


def main():
    matrix = np.zeros([len(characters)]*2)

    for line in sys.stdin.read().split('\n'):
        if '\t' in line:
            comb, count = line.split('\t')
            c1, c2 = comb.split('-')
            matrix[characters.index(c1), characters.index(c2)] = count

    matrix = matrix / matrix.sum()

    filename = sys.argv[1]
    np.savetxt(filename, matrix, fmt='%.8f')


if __name__ == '__main__':
    main()
