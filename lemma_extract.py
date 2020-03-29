# -*- coding: iso-8859-1 -*-
import numpy as np
import pandas as pd

import json

import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.es.stop_words import STOP_WORDS

from spacy import displacy

from tqdm import tqdm_notebook as tqdm
from pprint import pprint

from spacy.symbols import nsubj, VERB

# spanish lemmatizer
from spacy_spanish_lemmatizer import SpacyCustomLemmatizer


#
# Ver requirements.txt y ejecutar los install
# Ejecutar: python -m spacy download es_core_news_md
# Ejecutar: python -m spacy_spanish_lemmatizer download wiki
#
#

# see https://towardsdatascience.com/building-a-topic-modeling-pipeline-with-spacy-and-gensim-c5dc03ffc619
# see https://github.com/pablodms/spacy-spanish-lemmatizer
# see https://github.com/tokestermw/spacy_hunspell

#
# TODO: procesar en modo batch https://spacy.io/usage/processing-pipelines
# TODO: solo activar tokenizer, tagger y lemmatizer
#

from spacy_spellchecker import spaCySpellChecker


# read file
with open('conf/word_extract.json', 'r') as cfg_file:
    config = json.load(cfg_file)

comments = pd.read_csv('data/dump.csv', encoding='iso-8859-1', dtype=str)['comment']


def is_feature_token(token):
    # test if a token is a feature
    return token.is_stop != True and (token.lemma not in config['excluded_lemmas']) and (token.pos_ == 'NOUN' or token.pos_ == 'VERB' or token.pos_ == 'ADJ')

def is_valid_comment(c):
    # test if a token is a feature
    return  isinstance(c,str) and len(c) > 10

def collect_sentences(doc, collector):
    for s in doc.sents:
        words = list(map(lambda t: t.lemma_, filter(is_feature_token, s)))
        collector.append(words)

print('Loading spanish corpus ...')

nlp= spacy.load("es_core_news_md")

print ('Corpus loaded')

# add spell checker pipe
nlp.add_pipe(spaCySpellChecker(nlp, custom_dictionary=config['spell']), before="tagger")

# add spanish lemamtizer pipe
nlp.add_pipe(SpacyCustomLemmatizer(), name="lemmatizer", after="tagger")

#Se agrega sentencizer ya que no se hace analisis sintactico
nlp.add_pipe(nlp.create_pipe('sentencizer'))

# Updates spaCy's default stop words list with my additional words. 
nlp.Defaults.stop_words.update(config['stop_words'])
nlp.Defaults.stop_words.update(config['excluded_lemmas'])

# Iterates over the words in the stop words list and resets the "is_stop" flag.
for word in STOP_WORDS:
    lexeme = nlp.vocab[word]
    lexeme.is_stop = True

print('Processing comments...')

doc_list = []
# Iterates through each article in the corpus.
batch_result=nlp.pipe(filter(is_valid_comment,comments[0:100]), disable=["parser","ner"])
for r in batch_result:
    collect_sentences(r, doc_list)

from collections import Counter

counter=Counter()
for doc in doc_list:
    for word in doc:
        counter[word] += 1

print(counter)

