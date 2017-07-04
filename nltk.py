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
