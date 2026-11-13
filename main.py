"""MedResearch Phase 1 CLI - uses only the real dataset CSV."""
import argparse
import csv
from pathlib import Path
from preprocessing import preprocess
from inverted_index import build_inverted_index
from boolean_search import boolean_search
from ranked_search import RankedSearch

DEFAULT_CSV = Path(__file__).parent / 'dataset' / 'documents.csv'

def load_documents(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f'{path} missing. First run: python download_dataset.py --count 500')
    with path.open(encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        if not {'document_id','title','text'}.issubset(reader.fieldnames or []):
            raise ValueError('CSV must contain document_id,title,text')
        docs, ids, contents = [], set(), set()
        for row in reader:
            doc_id = (row['document_id'] or '').strip()
            title = (row['title'] or '').strip()
            body = (row['text'] or '').strip()
            if not doc_id or not body or doc_id in ids:
                continue
            content = (title.casefold(),body.casefold())
            if content in contents:
                continue
            if not preprocess(title + ' ' + body):
                continue
            ids.add(doc_id)
            contents.add(content)
            docs.append({'document_id':doc_id,'title':title,'text':body})
    if not docs:
        raise ValueError('No usable documents found')
    return docs

def demo(documents, index, ranker):
    print('\n== Preprocessing illustration ==')
    sample = documents[0]
    print('Document:', sample['document_id'], sample['title'])
    print('Original:', sample['text'][:180])
    print('Tokens (before stopwords / stemming):', preprocess(sample['title'] + ' ' + sample['text'][:180], False, False)[:30])
    print('Final terms:', preprocess(sample['title'] + ' ' + sample['text'][:180])[:30])
    print('\n== Inverted Index examples ==')
    for term in ['covid', 'vaccin', 'virus']:
        print(f'{term}: {sorted(index.get(term, set()))[:12]}')
    print('\n== Boolean demo ==')
    for q in ('covid AND vaccine', 'covid OR vaccine', 'covid AND NOT vaccine'):
        matches = boolean_search(q, index, {d['document_id'] for d in documents})
        print(f'{q} -> {len(matches)} matches, IDs: {sorted(matches)[:8]}')
    print('\n== Ranked queries ==')
    for q in ('covid vaccine immune response', 'respiratory infection treatment', 'coronavirus transmission prevention'):
        print('Query:', q)
        display_ranked(ranker.search(q, 3))

def display_ranked(results):
    if not results:
        print('  No positive similarity results.')
    for position, doc in enumerate(results, 1):
        print(f"  {position}. {doc['document_id']} (score={doc['score']:.4f}): {doc['title']}")
        print('     ', doc['text'][:175].replace('\n', ' '), '...')

def run(path: Path, demo_only=False):
    documents = load_documents(path)
    index = build_inverted_index(documents)
    ranker = RankedSearch(documents)
    all_ids = {d['document_id'] for d in documents}
    by_id = {d['document_id']: d for d in documents}
    print(f'MedResearch | indexed {len(documents)} biomedical articles | vocabulary {len(index)} terms')
    if demo_only:
        demo(documents,index,ranker)
        return
    while True:
        print('\n1. Boolean Search (AND / OR / NOT)\n2. Ranked Search (TF-IDF + Cosine)\n3. Preprocessing & demo evidence\n4. Exit')
        choice = input('Enter choice (1-4): ').strip()
        if choice == '4':
            print('Goodbye!')
            break
        if choice == '1':
            query = input('Boolean query: ').strip()
            try:
                matches = boolean_search(query,index,all_ids)
                print(f'Matching documents ({len(matches)}):')
                for doc_id in sorted(matches)[:30]:
                    print(f'  {doc_id}: {by_id[doc_id]["title"]}')
                if len(matches) > 30: print(f'  ... {len(matches)-30} more')
            except ValueError as err:
                print('Query error:',err)
        elif choice == '2':
            query = input('Ranked query: ').strip()
            display_ranked(ranker.search(query,5))
        elif choice == '3':
            demo(documents,index,ranker)
        else:
            print('Choose 1-4.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=Path, default=DEFAULT_CSV)
    parser.add_argument('--demo', action='store_true', help='Print repeatable examples then exit')
    args = parser.parse_args()
    run(args.dataset,args.demo)
