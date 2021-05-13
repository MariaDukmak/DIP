"""Mapper file that wil map the text to pairs of letters. """
import sys
from typing import TextIO
from const import ACCEPTED_CHARACTERS, CHARACTER_SPLITTER, SPACE

# The alphabet letters
accepted_characters = set(ACCEPTED_CHARACTERS)


def read_data(input_stream: TextIO) -> str:
    """
    Reads the file and removes any leading and trailing characters.
    :param input_stream: sys.stdin
    :return: generator object
    """
    for line in input_stream:
        yield line.strip()


def character_transform(character: str) -> str:
    """
    Transform unexpected character to a '!'. Also replace whitespaces with '_'.
    :param character: a string character
    :return: str of the new character
    """
    return '!' if character not in accepted_characters else character.replace(' ', SPACE)


def main():
    """
    Reads the file, split words in paris of letters and count it.
    """
    data = read_data(sys.stdin)
    for words in data:
        for index in range(len(words) - 1):
            c1, c2 = map(character_transform, words[index:index+2].lower())
            sys.stdout.write(f'{c1}{CHARACTER_SPLITTER}{c2}\t{1}\n')


if __name__ == "__main__":
    main()
