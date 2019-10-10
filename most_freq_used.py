from typing import Tuple

from index import Index, Entry

if __name__ == '__main__':
    index = Index()
    index.load("index.txt")
    words: Tuple[str, Entry] = index.most_freq_used(5)
    for word in words:
        print(word)
