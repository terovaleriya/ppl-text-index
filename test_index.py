import filecmp
import unittest

from index import Entry, Index


class EntryTests(unittest.TestCase):
    def test_add_page(self):
        entry = Entry()
        entry.add_page(5)
        entry.add_page(5)
        self.assertEqual(entry.pages, {5: 2})
        self.assertEqual(entry.count, 2)

    def test_init(self):
        entry = Entry(5, [(5, 2)])
        self.assertEqual(entry.pages, {5: 2})
        self.assertEqual(entry.count, 5)


class IndexTests(unittest.TestCase):
    def test_add_words(self):
        index = Index()
        index.add_word("Авдюшенко", 1)
        self.assertEqual(index.entries['Авдюшенко'], Entry(1, [(1, 1)]))
        index.add_word("Авдюшенко", 1)
        self.assertEqual(index.entries['Авдюшенко'], Entry(2, [(1, 2)]))
        index.add_word("Авдюшенко", 5)
        self.assertEqual(index.entries['Авдюшенко'], Entry(3, [(1, 2), (5, 1)]))

    def test_build(self):
        index = Index()
        index.build("test.txt")
        self.assertEqual(index.entries, {'баллов': Entry(1, [(1, 1)]),
                                         'были': Entry(1, [(1, 1)]),
                                         'было': Entry(1, [(1, 1)]),
                                         'можно': Entry(1, [(1, 1)]),
                                         'очень': Entry(1, [(1, 1)]),
                                         'получить': Entry(1, [(1, 1)]),
                                         'принципам': Entry(1, [(1, 1)]),
                                         'программирования': Entry(1, [(1, 1)]),
                                         'проекты': Entry(2, [(1, 2)])})

    def test_load(self):
        index = Index()
        index.load("test_index.txt")
        self.assertEqual(index.entries, {'Авдюшенко': Entry(2, [(1, 1), (28, 1)]),
                                         'Брагилевский': Entry(2, [(47, 1), (69, 1)]),
                                         'Карев': Entry(4, [(22, 1), (24, 1), (42, 1), (49, 1)]),
                                         'Кисляков': Entry(1, [(6, 1)]),
                                         'Сперанский': Entry(10, [(8, 2), (25, 1), (41, 1), (47, 1), (50, 1), (57, 1),
                                                                  (59, 1), (66, 1), (67, 1)]),
                                         'Степанов': Entry(7, [(12, 1), (17, 1), (30, 1), (48, 1), (53, 2), (54, 1)])})

    def test_most_freq_used(self):
        index = Index()
        index.load("test_index.txt")
        res = index.most_freq_used(1)
        self.assertEqual(res, [('Сперанский', Entry(10, [(8, 2), (25, 1), (41, 1), (47, 1), (50, 1), (57, 1),
                                                         (59, 1), (66, 1), (67, 1)]))])

    def test_save(self):
        index = Index()
        index.load("test_index.txt")
        index.save("test_index.tmp")
        self.assertTrue(filecmp.cmp("test_index.txt", "test_index.tmp"))


if __name__ == '__main__':
    unittest.main()
