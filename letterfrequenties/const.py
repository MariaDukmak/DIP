"""Defines the constants for this project."""
from pathlib import Path

SPACE = '_'
SPECIAL_CHARACTER = '!'
CHARACTER_SPLITTER = '-'

alphabet = 'abcdefghijklmnopqrstuwxyz'

# Characters that could be used for the mapper
ACCEPTED_CHARACTERS = alphabet + ' '
# Characters that could be used for the matrix
CHARACTERS = alphabet + SPACE + SPECIAL_CHARACTER

# Directory path to save the matrices
MATRIX_PATH = Path('trained_matrix')
