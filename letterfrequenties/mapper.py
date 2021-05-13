"""mapper."""
import sys

accepted_characters = set('abcdefghijklmnopqrstuwxyz ')


def read_data(file_name):
    for line in file_name:
        yield line.strip()


def character_transform(character):
    return '!' if character not in accepted_characters else character.replace(' ', '_')


def main():
    data = read_data(sys.stdin)
    for words in data:
        for index, word in enumerate(words[:-1].lower()):
            c1, c2 = map(character_transform, words[index:index+2])
            sys.stdout.write(f'{c1}-{c2}\t{1}\n')


if __name__ == "__main__":
    main()
