"""Mapper file that wil map the text to pairs of letters. """
import sys
from const import ACCEPTED_CHARACTERS, CHARACTER_SPLITTER, SPACE

# The alphabet letters
accepted_characters = set(ACCEPTED_CHARACTERS)


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
    for line in sys.stdin:
        for index in range(len(line) - 1):
            c1, c2 = map(character_transform, line[index:index+2].lower())
            sys.stdout.write(f'{c1}{CHARACTER_SPLITTER}{c2}\t{1}\n')


if __name__ == "__main__":
    main()
