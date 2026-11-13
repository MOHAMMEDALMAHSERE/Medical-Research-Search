# Phase 1 — Voice Presentation Outline (max 10 minutes)

The student guide's checklist requests a recorded voice presentation with each member speaking about 2 minutes and introducing themselves. Record this yourselves. This is a **script guide**, NOT a completed recorded submission.

## Speaker 1 — Problem, objectives & dataset (about 2 min)
"I'm [Name]. Our MedResearch project is a Python information retrieval system that searches medical research papers. It supports Boolean search and ranked search, not clinical diagnosis. We use the BEIR TREC-COVID corpus, searching title and text. Our objectives are to preprocess text consistently, retrieve exact matches using an inverted index, and rank the most relevant articles with TF-IDF and cosine similarity. My contribution was [actual work]."

## Speaker 2 — Dataset & NLP preprocessing (about 2 min)
"I'm [Name]. My contribution was [actual work]. We fetched [actual count] real documents, each with ID, title, and text. We filtered empty texts and duplicates, lowercased English text, tokenized, removed stopwords, and applied Porter stemming. Here is one before-and-after example from a real paper."

## Speaker 3 — Inverted index & Boolean (about 2 min)
"I'm [Name]. I worked on [actual work]. Our inverted index maps normalized terms to document ID sets. AND intersects postings, OR unions them, and NOT subtracts from the full indexed universe. Here are the real IDs from covid AND vaccine; covid OR vaccine; covid AND NOT vaccine. Boolean retrieval doesn't rank matches."

## Speaker 4 — TF-IDF & ranked search (about 2 min)
"I'm [Name]. I worked on [actual work]. The ranker creates TF-IDF vectors from the same corpus. For user queries, we reuse the fitted vectorizer and calculate cosine similarity. We sort by descending score and show document ID, title, and similarity. Here are three live query examples."

## Speaker 5 (if your team has five) — Integration & tests (about 2 min)
"I'm [Name]. I integrated [actual work] in main.py, ensured both retrieval methods use one corpus, and verified the project with automated tests and user search scenarios. The README includes reproducible setup commands. [Show real test output, commit evidence, demo.]"

**4-person team:** redistribute the integration and test material among the first four presenters. Do not claim an actual implementation or contribution not completed personally.
