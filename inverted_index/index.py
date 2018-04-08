import argparse
import json
import time

from collections import Counter, defaultdict
from string import punctuation

from lxml import objectify


_parser = objectify.makeparser(remove_blank_text=True)

# don't insert whitepsace when serializing to json
SEPARATORS = (',', ':')


def _tokenize(section):
    tokens = []
    for paragraph in section.P:
        tokens += paragraph.text.lower().split()

    return tokens


def _count(tokens, stoplist):
    term_counter = Counter()

    for token in tokens:
        token = token.strip(punctuation).strip()

        if stoplist and token in stoplist or not token:
            continue

        term_counter[token] += 1

    return term_counter


def _parse_article(article, stoplist):
    doc_id = article.DOCNO.text.strip()
    term_freqs = Counter()

    for section in ['HEADLINE', 'BYLINE', 'TEXT']:
        try:
            tokens = _tokenize(article[section])
            term_freqs += _count(tokens, stoplist)
        except AttributeError:
            # some documents might not have this section
            continue

    return doc_id, term_freqs, sum(term_freqs.values())


def _write(corpus_size, term_freq, doc_freq, doc_lengths,
           doc_lengths_fn='doc_lengths', lexicon_fn='lexicon',
           posting_fn='posting'):
    """

    Three files:
    1) document map: lines 1-N are: `docid` `doc_length`
    2) lexicon - lines 1 to N are: `term` `collection_freq`  `posting_pointer`
    3) posting file - each line is: term<docid, freq>, <docid, freq>
    """
    with open(doc_lengths_fn, 'w') as f:
        doc_map = dict(average=_avg_doc_length(doc_lengths),
                       documents=doc_lengths)
        json.dump(doc_map, f, separators=SEPARATORS)

    with open(lexicon_fn, 'w') as lexicon, open(posting_fn, 'w') as posting:
        lexicon.write('{}\n'.format(corpus_size))

        for term, idf in doc_freq.items():
            start_pos = posting.tell()
            posting.write('{}\n'.format(json.dumps(idf,
                                                   separators=SEPARATORS)))
            lexicon_entry = '{} {} {}\n'.format(term,
                                                term_freq[term],
                                                start_pos)
            lexicon.write(lexicon_entry)


def _load_xml(fn):
    with open(fn, 'r') as f:
        raw_xml = f.read().encode()  # need as  binary string
        return objectify.fromstring(raw_xml, parser=_parser)


def _load_stoplist(fn):
    with open(fn, 'r') as f:
        return {r.strip() for r in f}


def _avg_doc_length(doc_lengths):
    return int(sum(doc_lengths.values()) / len(doc_lengths))


def main(corpus, stoplist):
    # a set of words we don't care about (e.g. a, as, it, the etc...)
    stoplist = _load_stoplist(stoplist)

    # how often does a term appear in the overall collection?
    in_collection_freqs = Counter()

    # Contains the documents a term appears in, plus frequency in each document
    postings = defaultdict(list)

    doc_lengths = defaultdict(int)

    articles = _load_xml(corpus)
    corpus_size = len(articles.DOC)
    print('There are {} documents to index'.format(corpus_size))

    for article in articles.DOC:
        id, doc_freqs, doc_length = _parse_article(article, stoplist)
        doc_lengths[id] = doc_length
        in_collection_freqs += doc_freqs

        for word in doc_freqs:
            # TODO: can we avoid this inner loop?
            postings[word].append([id, doc_freqs[word]])

    _write(corpus_size, in_collection_freqs, postings, doc_lengths)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus')
    parser.add_argument('stoplist', default='stoplist')
    args = parser.parse_args()

    start = time.time()
    main(args.corpus, args.stoplist)
    end = time.time()
    print('Indexing complete in {} seconds'.format(end - start))
