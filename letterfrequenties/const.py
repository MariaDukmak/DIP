"""Defines the constants for this project."""
from pathlib import Path

# Characters that could be used for the mapper
ACCEPTED_CHARACTERS = 'abcdefghijklmnopqrstuwxyz '
# Characters that could be used for the matrix
CHARACTERS = 'abcdefghijklmnopqrstuwxyz_!'

SPACE_ALIAS = '_'
SPECIAL_CHARACTER_ALIAS = '!'
CHARACTER_SPLITTER = '-'

# Directory path to save the matrices
MATRIX_PATH = Path('trained_matrix')
