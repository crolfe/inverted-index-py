import argparse
import json
import operator

from collections import defaultdict, OrderedDict

from inverted_index.rank import bm25


def _posting_lookup(posting_file, offset):
    with open(posting_file) as f:
        f.seek(int(offset))
        return json.loads(f.readline().strip())


def process_query(terms, lexicon='lexicon', posting='posting',
                  stoplist='stoplist', doc_lengths='doc_lengths'):

    collection_size, lexicon = _load_lexicon(lexicon)
    avg_doc_length, doc_lengths = _load_doc_lengths(doc_lengths)

    doc_scores = defaultdict(float)

    for term in terms:
        if term in stoplist:
            continue

        try:
            print(term)
            entry = lexicon[term]
            print(entry)
        except KeyError:
            continue

        term_freq = entry['freq']
        posting_entries = _posting_lookup(posting, entry['offset'])

        for doc_id, doc_freq in posting_entries:
            # doc_id, doc_freq = doc
            doc_length = doc_lengths[doc_id]
            score = bm25(int(term_freq), int(doc_freq), doc_length,
                         avg_doc_length, collection_size)
            doc_scores[doc_id] += score

    doc_scores = OrderedDict(sorted(doc_scores.items(),
                                    key=operator.itemgetter(1),
                                    reverse=True))
    return doc_scores


def _load_lexicon(lexicon_file):
    lexicon = {}

    with open(lexicon_file) as f:
        corpus_size = f.readline()

        for line in f:
            term, freq, offset = line.strip().split(' ')
            lexicon[term] = dict(freq=freq, offset=offset)

        return int(corpus_size), lexicon


def _load_doc_lengths(doc_lengths_file):
    with open(doc_lengths_file) as f:
        data = json.load(f)

        return data['average'], data['documents']


if __name__ == '__main__':
    parser = argparse.ArgumentParser('search inverted index')
    parser.add_argument('terms', nargs='+')
    parser.add_argument('--lexicon', default='lexicon')
    parser.add_argument('--posting', default='posting')
    parser.add_argument('--stoplist', default='stoplist')
    parser.add_argument('--doc-lengths', default='doc_lengths')

    args = parser.parse_args()

    process_query(args.terms, args.lexicon, args.posting, args.stoplist,
                  args.doc_lengths)
