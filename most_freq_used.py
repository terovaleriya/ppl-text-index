from index import Index

if __name__ == '__main__':
    index = Index()
    index.load("index.txt")
    words = index.most_freq_used(5)
    for word in words:
        print(word)
