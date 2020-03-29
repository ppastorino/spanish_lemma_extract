# Spanish Lemma Extraction with Spacy

The objective of this application is to process a set of comments entered by web users and extract keywords from them.
The keywords later will be used to extract topics of interest to users

We have extended sPacy pipeline with 

- a spanish spell checker (based on https://github.com/pablodms/spacy-spanish-lemmatizer)
- a spanish lemmatizer  (based on https://pypi.org/project/pyspellchecker/)

The spell checker aims to correct user inputs wich have a lot of misppelled words.
The lemmatizer allows to extract lemmas that are more suitable than bare tokens for topic extraction.

Whe have enabled the following components of the processing pipeline:

- Tokenizer
- Sentencizer
- Tagger

The pourpouse of Sentencizer is divide the comments in smaller components. Each component may be related to different topics.
The pourpouse of Tagger is identify nouns, verbs and adjetives that are more relevant for topic extraction

Additionally we provide a configuration file to customize de process:

- Extend the spell checker with a custom dictionary
- Specify a stop word list to exlcude meaningless lemmas




