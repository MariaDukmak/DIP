"""mapper."""
import sys


def read_data(file_name):
    for line in file_name:
        yield line.strip()


def main():
    letters = set('abcdefghijklmnopqrstuwxyz ')
    data = read_data(sys.stdin)
    for words in data:
        for index, word in enumerate(words[:-1].lower()):
            l1 = '_' if words[index] not in letters else words[index]
            l2 = '_' if words[index+1] not in letters else words[index+1]
            l1.replace(' ', '#')
            l2.replace(' ', '#')
            sys.stdout.write(f'{l1}-{l2}\t{1}\n')


if __name__ == "__main__":
    main()
