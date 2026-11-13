"""Download reproducible first N valid TREC-COVID corpus records.
Official HF dataset: https://huggingface.co/datasets/BeIR/trec-covid
Primary: lightweight HF dataset viewer API; fallback: corpus.jsonl.gz.
"""
import argparse
import csv
import gzip
import io
import json
import urllib.parse
import urllib.request
from pathlib import Path

DATASET = 'BeIR/trec-covid'
FIELDS = ['document_id', 'title', 'text', 'source']
OUT = Path(__file__).parent / 'dataset' / 'documents.csv'

def valid_rows(records, n):
    ids, content, result = set(), set(), []
    for record in records:
        id_ = str(record.get('_id', record.get('document_id', ''))).strip()
        title = str(record.get('title') or '').strip()
        body = str(record.get('text') or '').strip()
        if not id_ or not body or id_ in ids:
            continue
        content_key = (title.casefold(), body.casefold())
        if content_key in content:
            continue
        ids.add(id_)
        content.add(content_key)
        result.append({'document_id': id_, 'title': title or f'Untitled article ({id_})',
                       'text': body, 'source': 'BeIR/trec-covid'})
        if len(result) >= n:
            break
    return result

def viewer_records():
    offset = 0
    while True:
        params = urllib.parse.urlencode({'dataset': DATASET, 'config': 'corpus',
                                         'split': 'corpus', 'offset': offset, 'length': 100})
        url = 'https://datasets-server.huggingface.co/rows?' + params
        with urllib.request.urlopen(url, timeout=50) as response:
            payload = json.load(response)
        rows = payload.get('rows', [])
        if not rows:
            break
        for item in rows:
            yield item['row']
        offset += len(rows)

def compressed_records():
    url = ('https://huggingface.co/datasets/BeIR/trec-covid/resolve/'
           'e068f9faf522968e3cdbb275c466c51edcaf4d1a/corpus.jsonl.gz')
    with urllib.request.urlopen(url, timeout=90) as response:
        with gzip.GzipFile(fileobj=response) as stream:
            for line in stream:
                if line.strip():
                    yield json.loads(line)

def save_dataset(n: int, out: Path = OUT):
    if n < 100:
        raise ValueError('Phase 1 requires at least 100 documents')
    problems = []
    for label, getter in [('dataset viewer API', viewer_records), ('corpus archive', compressed_records)]:
        try:
            records = valid_rows(getter(), n)
            if len(records) < n:
                raise ValueError(f'Only {len(records)} usable records were found')
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open('w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(records)
            print(f'Saved {len(records)} real TREC-COVID articles to {out} via {label}')
            return
        except Exception as exc:
            problems.append(f'{label}: {exc}')
    raise RuntimeError('Dataset download failed. Check internet access. ' + ' | '.join(problems))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=500)
    args = parser.parse_args()
    save_dataset(args.count)
