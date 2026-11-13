"""Term-to-set-of-document-IDs index (not a hardcoded search)."""
from collections import defaultdict
from preprocessing import preprocess

def build_inverted_index(documents: list[dict]) -> dict[str, set[str]]:
    index = defaultdict(set)
    for doc in documents:
        for term in set(preprocess(doc['title'] + ' ' + doc['text'])):
            index[term].add(doc['document_id'])
    return dict(index)
