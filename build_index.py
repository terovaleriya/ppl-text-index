from index import Index

if __name__ == '__main__':
    index = Index()
    index.build('Childhood.txt')
    index.save("index.txt")
