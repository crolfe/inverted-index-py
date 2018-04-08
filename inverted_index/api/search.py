import json
import os

from flask import request, Blueprint

from inverted_index.search import process_query


search_bp = Blueprint('api', __name__)
json_headers = {'Content-Type': 'application/json'}

posting = os.environ.get('POSTING_FILE', '/app/inverted_index/posting')
stoplist = os.environ.get('STOPLIST', '/app/inverted_index/stoplist.txt')
lexicon = os.environ.get('LEXICON', '/app/inverted_index/lexicon')


def ok(data=None):
    if not data:
        data = {}

    return json.dumps(data), 200, json_headers


def bad_request(err):
    resp = {'error': err}
    return json.dumps(resp), 400, json_headers


@search_bp.route('/search', methods=['GET'])
def search():
    terms = request.args.getlist('term')

    if not terms:
        return bad_request('No search terms were provided')

    results = process_query(terms, stoplist=stoplist, lexicon=lexicon,
                            posting=posting)

    return ok(results)
