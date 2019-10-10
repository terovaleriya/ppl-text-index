from index import Index

if __name__ == '__main__':
    index = Index()
    index.count_words('Childhood.txt')
    index.save("index.txt")
