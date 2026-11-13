"""Fit once on documents, transform queries with that same vectorizer."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import normalized

class RankedSearch:
    def __init__(self, documents: list[dict]):
        self.documents = documents
        self.vectorizer = TfidfVectorizer(lowercase=False, tokenizer=str.split,
                                          preprocessor=None, token_pattern=None,
                                          norm='l2', sublinear_tf=False)
        texts = [normalized(doc['title'] + ' ' + doc['text']) for doc in documents]
        if not any(texts):
            raise ValueError('No valid content to vectorize')
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        processed = normalized(query)
        if not processed:
            return []
        vector = self.vectorizer.transform([processed])  # never refit on the query
        similarities = cosine_similarity(vector, self.matrix).ravel()
        ranked = sorted(range(len(similarities)), key=lambda i: (-similarities[i], i))
        result = []
        for i in ranked:
            if similarities[i] <= 0 or len(result) >= top_k:
                break
            result.append({**self.documents[i], 'score': float(similarities[i])})
        return result
