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

# bigrams(['more', 'is', 'said', 'than', 'done'])
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

# 第五章
text = nltk.word_tokenize("And now for something completely different")
nltk.pos_tag(text)

# text.similar()方法为一个词w 找出所有上下文w1ww2，然后找出所有出现在相同上下文中的词w'，即w1w'w2
text2.similar('women')
# 词性 str2tuple
tagged_token = nltk.tag.str2tuple('fly/NN')

nltk.corpus.brown.tagged_words()
print(nltk.corpus.nps_chat.tagged_words())

# text 分类
from nltk.corpus import names
import random
def gender_features(word):
  return {'last_letter': word[-1]}
gender_features('Shrek')
names = ([(name, 'male') for name in names.words('male.txt')]+[(name, 'female') for name in names.words('female.txt')])
random.shuffle(names)
featuresets = [(gender_features(n), g) for (n,g) in names]
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)
classifier.classify(gender_features('Neo'))
classifier.classify(gender_features('Trinity'))
print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(5)

# ，使用函数nltk.classify.apply_features，返回一个行为像一个链表而不会在内存存储所有特征集的对象
from nltk.classify import apply_features
train_set = apply_features(gender_features, names[500:])
test_set = apply_features(gender_features, names[:500])

# 另一个分类的例子
from nltk.corpus import movie_reviews
documents = [(list(movie_reviews.words(fileid)), category)
    for category in movie_reviews.categories()
    for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words.keys())[:2000]

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
        return features
print(document_features(movie_reviews.words('pos/cv957_8737.txt')))
featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(5)

