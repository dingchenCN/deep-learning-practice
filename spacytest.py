import spacy
nlp = spacy.load('en')
doc = nlp(u'Hello, world. Here are two sentences.')
token = doc[0]
sentences = doc.sents
# sentence = sentences.__next__()
# sentence2 = sentences.__next__()
sentence = next(sentences)
sentence2 = next(sentences)
print(type(sentence))
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