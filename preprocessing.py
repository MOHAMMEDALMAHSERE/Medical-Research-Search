"""Shared deterministic English-language preprocessing."""
import re
from functools import lru_cache
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer

_STEMMER = PorterStemmer()

@lru_cache(maxsize=200000)
def _stem(term: str) -> str:
    return _STEMMER.stem(term)

def preprocess(text: str, remove_stopwords: bool = True, stem: bool = True) -> list[str]:
    tokens = re.findall(r"[a-z]+(?:'[a-z]+)?|\d+", str(text).lower())
    if remove_stopwords:
        tokens = [token for token in tokens if token not in ENGLISH_STOP_WORDS]
    if stem:
        tokens = [_stem(token) for token in tokens]
    return tokens

def normalized(text: str) -> str:
    return " ".join(preprocess(text))
