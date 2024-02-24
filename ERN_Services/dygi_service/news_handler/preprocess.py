import spacy

class SpacyTokenizer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")

    def docTokenizer(self, doc_input):

        doc_spacy = self.nlp(doc_input)
        sents= doc_spacy.sents
        doc_tokenized=[]

        for sent in sents:
            doc_tokenized.append([token.text for token in sent])

        return doc_tokenized
