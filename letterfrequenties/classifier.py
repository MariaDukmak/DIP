""""""
import sys
import numpy as np
import glob
import os
from const import MATRIX_PATH
from matrix_saver import to_matrix


def mse(matrix1: np.ndarray, matrix2: np.ndarray) -> float:
    return (np.square(matrix1 - matrix2)).mean()


"""
The Project Gutenberg EBook of Alice in Wonderland, by Lewis Carroll
This eBook is for the use of anyone anywhere at no cost and with almost no
van de toen bekende wereld. Op de kaden wemelde het van zeelieden,
terms of the Project Gutenberg License online at www.gutenberg.org

mapper ->
# engels-nederlands
1-0
1-0
0-1
1-0

reducer ->

3-1
"""


def scanner():
    classes = {os.path.basename(path).replace('.txt', ''): np.loadtxt(path) for path in glob.glob(str(MATRIX_PATH / '*.txt'))}
    counter = np.zeros(len(classes), dtype=np.int)
    for line in sys.stdin:
        row = line.rstrip('\n')
        # Hallo dit is een zin
        # h-i 2
        # l-o 3
        matrix = to_matrix(row)
        min_index = np.argmin(np.array(mse(matrix, class_matrix) for class_matrix in classes.values()))
        counter[min_index] += 1

    for language, count in zip(classes.keys(), counter):
        print(f"{language}: \t{count}")


def main():
    predict_matrix: np.ndarray = to_matrix(sys.stdin.read())
    train_matrices = map(np.loadtxt, glob.glob(str(MATRIX_PATH / '*.txt')))
    # scanner()
    losses = np.array([mse(predict_matrix, train_matrix) for train_matrix in train_matrices])
    soft_max = ((1/losses) / (1/losses).sum())
    for language_path, confidence in zip(glob.glob(str(MATRIX_PATH / '*.txt')), soft_max):
        print(f"{os.path.basename(language_path)}:\t{confidence*100:.2f}%")


if __name__ == '__main__':
    main()
