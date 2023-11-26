import itertools
import string

# Create an iterator that generates 3-character combinations of ASCII letters
combinations = itertools.product(string.ascii_letters, repeat=3)

# Let's say we have a list of 10,000 words
words = ["hello", "amma", "can"]  # replace with your list of words

# Create a dictionary that maps words to 3-character sequences
word_to_encoding = {word: ''.join(next(combinations)) for word in words}

# Now you can encode a word like this:
word = "hello"
encoded_word = word_to_encoding[word]
print(encoded_word)  # prints "abc"

