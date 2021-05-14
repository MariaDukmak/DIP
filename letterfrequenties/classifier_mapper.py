"""Maps each line of the text to make a matrix of it."""
import sys
import glob
import numpy as np
from const import CHARACTERS, MATRIX_PATH
from trainer_mapper import character_transform


def mse(matrix1: np.ndarray, matrix2: np.ndarray) -> float:
    return (np.square(matrix1 - matrix2)).mean()


def main():
    """
    Reads the input, split the letters in pairs for each line and choose a language.
    """
    matrices = list(map(np.loadtxt, glob.glob(str(MATRIX_PATH / '*.txt'))))

    for line in sys.stdin:
        if len(line) > 1:
            matrix = np.zeros([len(CHARACTERS)] * 2)

            for index in range(len(line) - 1):
                c1, c2 = map(character_transform, line[index:index+2].lower())
                matrix[CHARACTERS.index(c1), CHARACTERS.index(c2)] += 1

            normalized_matrix = matrix / matrix.sum()

            min_index = np.argmin(np.array([mse(normalized_matrix, class_matrix) for class_matrix in matrices]))
            one_hot_vector = np.zeros(len(matrices), dtype=np.int)
            one_hot_vector[min_index] = 1
            sys.stdout.write(f"{'-'.join(map(str, one_hot_vector))}\n")


if __name__ == "__main__":
    main()
