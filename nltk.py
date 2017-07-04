import nltk

from nltk.book import *

text1.concordance("monstrous")
text1.similar("monstrous")
text2.common_contexts(["monstrous", "very"])
text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])
text3.generate()

len(text3)
sorted(set(text3))
len(set(text3))
text3.count("smote")
100 * text4.count('a') / len(text4)
len(text3) / len(set(text3))
text4[173]
text4.index('awaken')
text5[16715:16735]
text4[173][0]
' '.join(['Monty', 'Python'])
'Monty Python'.split()

fdist1 = FreqDist(text1) #计算词频 返回dict
fdist1['whale']

fdist1.plot(50, cumulative=True)
fdist1.hapaxes() # 只出现了一次的词（所谓的hapaxes）

V = set(text1)
long_words = [w for w in V if len(w) > 15]
sorted(long_words)

fdist5 = FreqDist(text5)
sorted([w for w in set(text5) if len(w) > 7 and fdist5[w] > 7])

bigrams(['more', 'is', 'said', 'than', 'done'])
text4.collocations()

[len(w) for w in text1]
fdist = FreqDist([len(w) for w in text1])
fdist.keys()
fdist.items()
fdist.max()
fdist[3]
fdist.freq(3)

[w for w in sent7 if len(w) < 4]
[w for w in sent7 if len(w) <= 4]

sorted([w for w in set(text7) if '-' in w and 'index' in w])

nltk.chat.chatbots()

sorted([w for w in set(text5) if w.startswith('b')])

