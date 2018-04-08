import argparse


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
index_parser = subparsers.add_parser('index', help='index help')
index_parser.add_argument('-s', help='use stoplist', action='store_true')
index_parser.add_argument('corpus',
                          help='file containing the documents to be parsed')

search_parser = subparsers.add_parser('search', help='search help')


def main(args=None):
    print(vars(parser.parse_args()))


if __name__ == '__main__':
    main()
