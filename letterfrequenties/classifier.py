""""""
import sys
import numpy as np
import glob
import os
from const import MATRIX_PATH
from matrix_saver import to_matrix


def mse(matrix1, matrix2) -> float:
    return (np.square(matrix1 - matrix2)).mean()


def main():
    predict_matrix: np.ndarray = to_matrix(sys.stdin.read())
    train_matrices = map(np.loadtxt, glob.glob(str(MATRIX_PATH / '*.txt')))
    losses = np.array([mse(predict_matrix, train_matrix) for train_matrix in train_matrices])
    soft_max = ((1/losses) / (1/losses).sum())
    for language_path, confidence in zip(glob.glob(str(MATRIX_PATH / '*.txt')), soft_max):
        print(f"{os.path.basename(language_path)}:\t{confidence*100:.2f}%")


if __name__ == '__main__':
    main()
