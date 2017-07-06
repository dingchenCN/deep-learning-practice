import textacy
from textacy import datasets

cw = datasets.CapitolWords()
records = cw.records(speaker_name={'Hillary Clinton', 'Barack Obama'})
text_stream, metadata_stream = textacy.fileio.split_record_fields(records, 'text')
corpus = textacy.Corpus('en', texts=text_stream, metadatas=metadata_stream)
print(corpus)

doc_term_matrix, id2term = textacy.vsm.doc_term_matrix(
    (doc.to_terms_list(ngrams=1, named_entities=True, as_strings=True)
     for doc in corpus),
    weighting='tfidf', normalize=True, smooth_idf=True, min_df=2, max_df=0.95)
print(repr(doc_term_matrix))
