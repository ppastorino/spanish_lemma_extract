from __future__ import unicode_literals
from spellchecker import SpellChecker
from spacy.tokens import Doc, Span, Token


class spaCySpellChecker(object):

    def __init__(self, nlp, custom_dictionary):
        Token.set_extension('spellchecker_unknown', default=None)
        self.checker = SpellChecker(language='es')
        self.custom_dictionary = custom_dictionary 

    def __call__(self, doc):
        correct_words = []
        for token in doc:
            text = self.custom_dictionary.get(token.text,token.text)
            try:
                misspelled = self.checker.unknown([text])
                if misspelled:
                    word = next(iter(misspelled))
                    correct = self.checker.correction(word)
                    correct_words.append(correct)
                else:
                    correct_words.append(text)
                
            except UnicodeEncodeError:
                pass
        return Doc(doc.vocab, words=correct_words)

