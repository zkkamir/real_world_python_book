import sys
import os
import random
from collections import defaultdict, Counter

from matplotlib.pyplot import text

filepath = os.path.dirname(__file__)


def load_file(infile):
    """Read and return text file as a list of
       lowercase words without punctuation."""
    with open(infile) as f:
        words = [word.lower() for line in f for word in line.split()]
        words_no_punct = ["".join(char for char in word if char.isalpha())
                          for word in words]
    return words_no_punct


def make_dict(text, shift):
    """Return dictionary of words and shifted indexes."""
    word_dict = defaultdict(list)
    for index, word in enumerate(text):
        word_dict[word].append(index + shift)
    return word_dict


def encrypt(message, word_dict):
    """Return list of indexes representing words in a message."""
    encrypted = []
    for word in message.lower().split():
        if len(word_dict[word]) > 1:
            index = random.choice(word_dict[word])
        elif len(word_dict[word]) == 1:  # Random.choice fails if only 1 choice
            index = word_dict[word][0]
        elif len(word_dict[word]) == 0:
            print("\nCharacter {} not in dictionary.".format(word),
                  file=sys.stderr)
            continue
        encrypted.append(index)
    return encrypted


def decrypt(message, text, shift):
    """Decrypt ciphertext list and return plaintext string."""
    plaintext = []
    indexes = [s.replace(",", "").replace("[", "").replace("]", "")
               for s in message.split()]
    for i in indexes:
        plaintext.append(text[int(i) - shift])
    return " ".join(plaintext)


def check_for_fail(ciphertext):
    """Return True if ciphertext contains any duplicate keys."""
    check = [k for k, v in Counter(ciphertext).items() if v > 1]
    if len(check) > 0:
        return True


def main():
    message = input("Enter plaintext or ciphertext: ")
    process = input("Enter 'encrypt or 'decrypt': ")
    while process not in ("encrypt", "decrypt"):
        process = input("Enter 'encrypt or 'decrypt': ")
    shift = int(input("Shift value. Enter digit from 1 to 366: "))
    while not 1 <= shift <= 366:
        shift = int(input("Shift value. Enter digit from 1 to 366: "))
    infile = input("Enter filename with extension: ")
    infile = os.path.join(filepath, infile)
    if not os.path.exists(infile):
        print("File {} not found. Terminating.".format(infile), file=sys.stderr)
        sys.exit(1)

    text = load_file(infile)
    word_dict = make_dict(text, shift)

    if process == "encrypt":
        ciphertext = encrypt(message, word_dict)
        if check_for_fail(ciphertext):
            print("\nProblem finding unique keys.", file=sys.stderr)
            print("Try again, change message, or change code book.\n",
                  file=sys.stderr)
            sys.exit()
        # print("\nCharacter and number of occurences in word_dict: \n")
        # print("{: >10}{: >10}{: >10}".format("Character", "Unicode", "Count"))
        # for key in sorted(word_dict.keys()):
        #     print("{: >10}{: >10}{: >10}".format(repr(key)[1:-1],
        #                                          str(ord(key)),
        #                                          len(word_dict[key])))
        # print("\nNumber of distinct characters: {}".format(len(word_dict)))
        # print("Total number of characters: {:,}\n".format(len(text)))

        print("encrypted ciphertext = \n {}\n".format(ciphertext))

    elif process == "decrypt":
        plaintext = decrypt(message, text, shift)
        print("\ndecrypted plaintext = \n {}".format(plaintext))


if __name__ == "__main__":
    main()
