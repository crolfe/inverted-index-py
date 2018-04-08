from math import log

# BM25 constants
k1 = 1.2
b = 0.75


def bm25(term_freq, doc_freq, doc_length, avg_doc_length, collection_size):
    """
    See: https://en.wikipedia.org/wiki/Okapi_BM25#The_ranking_function

    term_freq: frequency of term across entire collection
    doc_freq: frequency of term in a single document
    doc_length: length of a single document (in words)
    avg_doc_length: used to prevent longer documents from appearing more
                    relevant, simply because they contain more terms
    """
    N = collection_size

    K = k1 * ((1 - b) + b * (doc_length / avg_doc_length))

    inverse_doc_freq = log(((N - term_freq + 0.5) / (term_freq + 0.5)))

    return inverse_doc_freq * ((k1 + 1) * doc_freq) / (K + doc_freq)
