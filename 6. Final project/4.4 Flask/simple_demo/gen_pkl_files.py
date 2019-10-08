import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

train = pd.read_csv('products_sentiment_train.tsv', sep='\t', names=['reviews', 'label'])
vectorizer = TfidfVectorizer(max_df=0.3, ngram_range=(1, 3))
classifier = LogisticRegression(C=1000)
classifier.fit(vectorizer.fit_transform(train.reviews), train.label)
with open('LogisticTextSentiment.pkl', 'wb') as c, open('Vectorizer.pkl', 'wb') as v:
    pickle.dump(vectorizer, v)
    pickle.dump(classifier, c)

