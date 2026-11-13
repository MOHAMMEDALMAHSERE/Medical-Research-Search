"""Tiny synthetic fixtures for CODE verification only; not the Phase 1 dataset."""
import unittest
from preprocessing import preprocess
from inverted_index import build_inverted_index
from boolean_search import boolean_search
from ranked_search import RankedSearch

DOCS = [
    {'document_id':'D1','title':'COVID Vaccine','text':'Covid vaccine immunity and immune response'},
    {'document_id':'D2','title':'COVID Transmission','text':'Coronavirus transmission prevention'},
    {'document_id':'D3','title':'Cancer Treatment','text':'Cancer treatment and chemotherapy'},
    {'document_id':'D4','title':'Vaccine Research','text':'Vaccine immune response research'},
]
class SearchTests(unittest.TestCase):
    def setUp(self):
        self.index = build_inverted_index(DOCS)
        self.ids = {d['document_id'] for d in DOCS}
    def test_preprocessing(self):
        self.assertIn('vaccin', preprocess('Vaccines and VACCINE'))
        self.assertNotIn('and', preprocess('Vaccines and Vaccine'))
    def test_and(self):
        self.assertEqual(boolean_search('covid AND vaccine', self.index,self.ids), {'D1'})
    def test_or(self):
        self.assertEqual(boolean_search('covid OR vaccine', self.index,self.ids), {'D1','D2','D4'})
    def test_not(self):
        self.assertEqual(boolean_search('covid AND NOT vaccine', self.index,self.ids), {'D2'})
    def test_precedence(self):
        self.assertEqual(boolean_search('covid OR cancer AND NOT vaccine',self.index,self.ids), {'D1','D2','D3'})
        self.assertEqual(boolean_search('(covid OR cancer) AND NOT vaccine',self.index,self.ids), {'D2','D3'})
    def test_ranked(self):
        ranker = RankedSearch(DOCS)
        ranked = ranker.search('vaccine immunity',2)
        self.assertEqual(ranked[0]['document_id'],'D1')
        self.assertGreater(ranked[0]['score'],0)
        self.assertLessEqual(ranked[0]['score'],1)
    def test_empty(self):
        self.assertEqual(RankedSearch(DOCS).search('the and'),[])
        with self.assertRaises(ValueError):
            boolean_search('', self.index,self.ids)

if __name__ == '__main__': unittest.main()
