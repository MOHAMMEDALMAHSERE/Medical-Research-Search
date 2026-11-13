# MedResearch — Medical Research Search Engine (Phase 1)

Al al-Bayt University | Information Retrieval Systems (902333)

## What it does
Python console search over actual biomedical paper **titles + abstracts/text** from [TREC-COVID (BEIR)](https://huggingface.co/datasets/BeIR/trec-covid). One document collection powers both retrieval paths:

- **Inverted index:** Python dict mapping normalized term -> set of document IDs, with AND, OR, NOT, parentheses. Boolean retrieval produces exact matching ID sets.
- **Ranked search:** scikit-learn TF-IDF document vectors; query transformed with the SAME already fitted vectorizer; cosine similarity; descending top-k articles, IDs, titles, and scores.

> Scope: lexical document retrieval, not diagnosis, clinical advice, semantic search, or a trained LLM.

## Run on Windows / VS Code
Open terminal **inside this extracted folder**:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
```

Repeatable evidence (prints preprocessing and 3 Boolean + 3 ranked searches):

```powershell
python main.py --demo
python -m unittest discover -s tests -v
```

Linux / macOS: use `python3 -m venv .venv`, `source .venv/bin/activate`, `python3 ...`.

**Internet required once** to download source documents. Downloader first calls the official HF dataset viewer in 100-row pages; if unavailable, streams the original `corpus.jsonl.gz`. If network policy blocks both, fetch source corpus manually using the link below and rerun from a network-connected machine.

## Document records
`dataset/documents.csv`: document_id (source `_id`), title, text, source. We load the first 500 distinct usable records in original corpus order, removing records with empty text, duplicate IDs, and exact duplicate title/body pairs. Script is deterministic when source ordering is unchanged. No fabricated Phase-1 dataset is supplied.

## Preprocessing
Lowercasing -> regex tokenization -> English stopword removal (scikit-learn built-in) -> Porter stemming (NLTK). Same `preprocess()` is used for indexing, Boolean query terms and TF-IDF text. `main.py --demo` prints original text, original tokens and final terms for a real record.

## Boolean syntax
Examples: `covid AND vaccine`, `covid OR vaccine`, `covid AND NOT vaccine`, `(covid OR cancer) AND NOT vaccine`. Operator precedence: NOT > AND > OR. Boolean terms are preprocessed consistently with corpus. No implicit AND between separate words: use operators. NOT operates relative to **all indexed document IDs**. Out-of-vocabulary terms return an empty set. Invalid / empty expressions produce a helpful error.

## Ranked retrieval
Run examples: `covid vaccine immune response`, `respiratory infection treatment`, `coronavirus transmission prevention`. TF-IDF fit ONCE for entire corpus; query vector obtained via `.transform()`. Show up to top-5 scores `> 0`; if none, show no results. Similarity scores depend on the actual downloaded corpus and are NOT hardcoded. A 500-document first-record sample may produce few COVID-specific matches because corpus ordering is not topical; this is expected.

## Evidence and reproducibility
`python main.py --demo > evidence/real_dataset_demo.txt` (run AFTER actual download) and `python -m unittest discover -s tests -v > evidence/tests.txt 2>&1`. Screenshots can show main menu, index sample postings, 3 Boolean queries and 3 ranked queries. Tests contain a tiny **synthetic unit-test fixture** used exclusively for implementation checks, NOT as the submitted document collection.

## Team contributions (complete truthfully)
Assign 4–5 actual people and record contribution links/commits in `TEAM_PROGRESS.md`. The template is blank by design; fabricated contributions are unacceptable.

## Dataset and license
- Dataset: BeIR TREC-COVID, original biomedical retrieval corpus (English), citation: BEIR benchmark (Thakur et al., 2021); scientific paper retrieval benchmark.
- URL: https://huggingface.co/datasets/BeIR/trec-covid
- Corpus fields: `_id`, `title`, `text`.
- Dataset card states CC BY-SA 4.0; comply with attribution and applicable sharing terms.
- This tool is for document retrieval, not treatment suggestions.

## Suggested file map
- `download_dataset.py` — acquire and clean 500 real articles
- `preprocessing.py` — shared NLP steps
- `inverted_index.py` — Python dict and sets
- `boolean_search.py` — actual AND, OR, NOT set operations
- `ranked_search.py` — TF-IDF and cosine similarity
- `main.py` — integrated menu & example outputs
- `tests/` — automated correctness tests using synthetic mini-fixture
- `phase1_proposal.pdf` — project proposal, complete member names before submitting
- `TEAM_PROGRESS.md` — fill in real student roles, commits, milestone dates and evidence
- `VIDEO_SCRIPT.md` — approximately 2-minute speaking prompts per member; actual recording must be completed by students

## Implementation cautions
- **Real paper retrieval results need actual downloaded corpus.** Testing with a fixture only verifies logic; it is not evidence of 100+ real records.
- Only legitimate team members should assert completing tasks or tests; don't claim video is recorded before recording.
