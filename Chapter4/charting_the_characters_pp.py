import os.path

from collections import Counter
import matplotlib.pyplot as plt


FILEPATH = os.path.dirname(__file__)


def load_file(infile):
    """Read and return a text file as a string of lowercase characters."""
    with open(os.path.join(FILEPATH, infile)) as f:
        loaded_string = f.read().lower()
    return loaded_string


str = load_file("lost.txt")

character_count = Counter(str).most_common()

x_axis = []
y_axis = []

for i in character_count:
    x_axis.append(i[0])
    y_axis.append(i[1])

plt.bar(x_axis, y_axis)
plt.title("A chart of frequency of characters in 'The Lost World'")
plt.show()
