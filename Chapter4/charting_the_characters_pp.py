import sys
import os
import operator
from collections import Counter
import matplotlib.pyplot as plt


FILEPATH = os.path.dirname(__file__)


def load_file(infile):
    """Read and return text file as string of lowercase characters."""
    with open(os.path.join(FILEPATH, infile)) as f:
        text = f.read().lower()
    return text


def main():
    infile = 'lost.txt'
    if not os.path.exists(os.path.join(FILEPATH, infile)):
        print("File {} not found. Terminating.".format(infile),
              file=sys.stderr)
        sys.exit(1)

    text = load_file(infile)

    # Make bar chart of characters in text and their frequency.
    char_freq = Counter(text)
    char_freq_sorted = sorted(char_freq.items(),
                              key=operator.itemgetter(1), reverse=True)
    x, y = zip(*char_freq_sorted)  # * unpacks iterable.
    fig, ax = plt.subplots()
    ax.bar(x, y)
    fig.show()


if __name__ == '__main__':
    main()
