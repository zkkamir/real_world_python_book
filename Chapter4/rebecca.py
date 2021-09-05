import sys
import os
import random
from collections import defaultdict, Counter

from matplotlib.pyplot import text

filepath = os.path.dirname(__file__)


def load_file(infile, encoding='utf-8', errors='ignore'):
    """Read and return text file as a string of lowercase characters."""
    with open(infile) as f:
        loaded_string = f.read().lower()
    return loaded_string


def make_dict(text, shift):
    """Return dictionary of characters and shifted indexes."""
    char_dict = defaultdict(list)
    for index, char in enumerate(text):
        char_dict[char].append(index + shift)
    return char_dict


def encrypt(message, char_dict):
    """Return list of indexes representing characters in a message."""
    encrypted = []
    for char in message.lower():
        if len(char_dict[char]) > 1:
            index = random.choice(char_dict[char])
        elif len(char_dict[char]) == 1:  # Random.choice fails if only 1 choice
            index = char_dict[char][0]
        elif len(char_dict[char]) == 0:
            print("\nCharacter {} not in dictionary.".format(char),
                  file=sys.stderr)
            continue
        encrypted.append(index)
    return encrypted


def decrypt(message, text, shift):
    """Decrypt ciphertext list and return plaintext string."""
    plaintext = ""
    indexes = [s.replace(",", "").replace("[", "").replace("]", "")
               for s in message.split()]
    for i in indexes:
        plaintext += text[int(i) - shift]
    return plaintext


def check_for_fail(ciphertext):
    """Return True if ciphertext contains any duplicate keys."""
    check = [k for k, v in Counter(ciphertext).items() if v > 1]
    if len(check) > 0:
        return True


def main():
    message = input("Enter plaintext or ciphertext: ")
    process = input("Enter 'encrypt or 'decrypy': ")
    while process not in ("encrypt", "decrypy"):
        process = input("Enter 'encrypt or 'decrypy': ")
    shift = int(input("Shift value. Enter digit from 1 to 366: "))
    while not 1 <= shift <= 366:
        shift = int(input("Shift value. Enter digit from 1 to 366: "))
    infile = input("Enter filename with extension: ")
    infile = os.path.join(filepath, infile)
    if not os.path.exists(infile):
        print("File {} not found. Terminating.".format(infile), file=sys.stderr)
        sys.exit(1)

    text = load_file(infile)
    char_dict = make_dict(text, shift)

    if process == "encrypt":
        ciphertext = encrypt(message, char_dict)
        if check_for_fail(ciphertext):
            print("\nProblem finding unique keys.", file=sys.stderr)
            print("Try again, change message, or change code book.\n",
                  file=sys.stderr)
            sys.exit()
        print("\nCharacter and number of occurences in chart_dict: \n")
        print("{: >10}{: >10}{: >10}".format("Character", "Unicode", "Count"))
        for key in sorted(char_dict.keys()):
            print("{: >10}{: >10}{: >10}".format(repr(key)[1:-1],
                                                 str(ord(key)),
                                                 len(char_dict[key])))
        print("\nNumber of distinct characters: {}".format(len(char_dict)))
        print("Total number of characters: {:,}\n".format(len(text)))

        print("encrypted ciphertext = \n {}\n".format(ciphertext))
        print("decrypted plaintext = ")

        for i in ciphertext:
            print(text[i - shift], end="", flush=True)

    elif process == "decrypt":
        plaintext = decrypt(message, text, shift)
        print("\ndecrypted plaintext = \n {}".format(plaintext))


if __name__ == "__main__":
    main()