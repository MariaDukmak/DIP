"""mapper."""
import sys
from typing import TextIO
from const import ACCEPTED_CHARACTERS, CHARACTER_SPLITTER, SPACE_ALIAS

accepted_characters = set(ACCEPTED_CHARACTERS)


def read_data(file_name: TextIO):
    for line in file_name:
        yield line.strip()


def character_transform(character: str):
    return '!' if character not in accepted_characters else character.replace(' ', SPACE_ALIAS)


def main():
    data = read_data(sys.stdin)
    for words in data:
        for index in range(len(words) - 1):
            c1, c2 = map(character_transform, words[index:index+2].lower())
            sys.stdout.write(f'{c1}-{c2}\t{1}\n')


if __name__ == "__main__":
    main()
