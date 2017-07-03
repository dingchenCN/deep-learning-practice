import spacy
nlp = spacy.load('en')
doc = nlp(u'Hello, world. Here are two sentences.')
token = doc[0]
sentences = doc.sents
# sentence = sentences.__next__()
# sentence2 = sentences.__next__()
sentence = next(sentences)
sentence2 = next(sentences)
# print(type(sentence))
# https://spacy.io/docs/usage/data-model
assert token is sentence[0]
assert sentence.text == 'Hello, world.'

hello_id = nlp.vocab.strings['Hello']
hello_str = nlp.vocab.strings[hello_id]

assert token.orth_ == hello_str == 'Hello'
assert token.orth == hello_id == 6747

assert token.shape_ == 'Xxxxx'
for lexeme in nlp.vocab:
    if lexeme.is_alpha:
        lexeme.shape_ = 'W'
    elif lexeme.is_digit:
        lexeme.shape_ = 'D'
    elif lexeme.is_punct:
        lexeme.shape_ = 'P'
    else:
        lexeme.shape_ = 'M'
assert token.shape_ == 'W'

from spacy.attrs import ORTH, LIKE_URL, IS_OOV

attr_ids = [ORTH, LIKE_URL, IS_OOV]
doc_array = doc.to_array(attr_ids)
assert doc_array.shape == (len(doc), len(attr_ids))
assert doc[0].orth == doc_array[0, 0]
assert doc[1].orth == doc_array[1, 0]
assert doc[0].like_url == doc_array[0, 1]
assert list(doc_array[:, 1]) == [t.like_url for t in doc]

doc = nlp("Apples and oranges are similar. Boots and hippos aren't.")

apples = doc[0]
oranges = doc[2]
boots = doc[6]
hippos = doc[8]

assert apples.similarity(oranges) >= boots.similarity(hippos)

