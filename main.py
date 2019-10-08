import re
import string
from collections import defaultdict
from typing import Set, Dict


class Entry:
    pages = Dict[int, int]
    count: int

    def __init__(self):
        self.pages = defaultdict(lambda: 0)
        self.count = 0

    def add_page(self, page: int):
        self.pages[page] = self.pages[page] + 1
        self.count = self.count + 1

    def __repr__(self) -> str:
        return str(self.count)


class Index:
    entries: Dict[str, Entry]

    def __init__(self):
        self.entries = defaultdict(lambda: Entry())

    def add_word(self, word: str, page: int):
        entry = self.entries[word]
        entry.add_page(page)

    def count_words(self, filename: str):
        with open(filename, 'rt') as fp:
            for cnt, line in enumerate(fp):
                words = re.sub('[' + string.punctuation + string.ascii_letters + 'à-ö0-9]', '', line.lower()).split()
                words = set(words) - {"и", "а", "в", "я", "на", "не", "что", "с", "она", "они", "оно", "он", "как",
                                      "мне", "меня",
                                      "но", "его", "ее", "это", "к", "так", "за", "по", "же"}
                page = cnt // 45 + 1
                for word in words:
                    index.add_word(word, page)

    def save(self, filename: str):
        with open(filename, 'w') as fp:
            for entry in sorted(self.entries.items()):
                k, v = entry
                fp.write(k + ":" + " ")
                fp.write(str(v.count) + ":" + " ")
                for page, count in sorted(v.pages.items()):
                    fp.write(str(page))
                    if count > 1:
                        fp.write("(" + str(count) + ")")
                    fp.write(", ")
                fp.write("\n")


if __name__ == '__main__':
    index = Index()
    index.count_words('Childhood.txt')
    index.save("index.txt")
