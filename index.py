import re
import string
from collections import defaultdict
from typing import Dict, Tuple

skip_words = {"и", "а", "в", "я", "на", "не", "что",
              "с", "она", "они", "оно", "он", "как",
              "мне", "меня", "но", "его", "ее", "это",
              "к", "так", "за", "по", "же", "из", "то",
              "о", "от"}


class Entry:
    pages = Dict[int, int]
    count: int

    def __init__(self, count=0, pages=None):
        self.pages = defaultdict(lambda: 0)
        self.count = count
        if pages is not None:
            for p, c in pages:
                self.pages[p] = c

    def add_page(self, page: int):
        self.pages[page] = self.pages[page] + 1
        self.count = self.count + 1

    def __repr__(self) -> str:
        def format_pages(x: Tuple[int, int]) -> str:
            page, count = x
            return str(page) + ('(' + str(count) + ')' if count > 1 else '')

        pages = ', '.join(map(format_pages, self.pages.items()))
        return str(self.count) + ', ' + pages


class Index:
    number_of_lines_per_page: int
    entries: Dict[str, Entry]

    def __init__(self):
        self.entries = defaultdict(lambda: Entry())
        self.number_of_lines_per_page = 45

    def add_word(self, word: str, page: int):
        entry = self.entries[word]
        entry.add_page(page)

    def count_words(self, filename: str):
        with open(filename, 'rt') as fp:
            for cnt, line in enumerate(fp):
                words = re.sub('[' + string.punctuation + string.ascii_letters + 'à-ö0-9]', '', line.lower()).split()
                words = set(words) - skip_words
                page = cnt // self.number_of_lines_per_page + 1
                for word in words:
                    self.add_word(word, page)

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

    @staticmethod
    def read_pages(t: Tuple[str, str]):
        if t[1]:
            return int(t[0]), int(t[1])
        else:
            return int(t[0]), 1

    def load(self, filename: str):
        with open(filename, 'rt') as fp:
            for line in fp:
                word, count, pstr = line.split(":")
                pages = list(map(self.read_pages, re.findall(r'(\d+)(?:\((\d+)\))?, ', pstr)))
                entry = Entry(int(count), pages)
                self.entries[word] = entry  # pages

    def most_freq_used(self, count: int) -> Tuple[str, Entry]:
        swords: Tuple[str, Entry] = sorted(self.entries.items(), key=lambda kv: -kv[1].count)
        return swords[:count]
