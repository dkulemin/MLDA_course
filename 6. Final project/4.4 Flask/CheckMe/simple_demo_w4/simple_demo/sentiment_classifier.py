from sklearn.externals import joblib
from nltk.stem.porter import PorterStemmer
import re, os

class SentimentClassifier(object):

    def __init__(self):
        self.model = joblib.load(os.path.join('model', 'clf.pkl'))
        self.vectorizer = joblib.load(os.path.join('model', 'vect.pkl'))
        self.classes_dict = {0:'negative', 1:'positive'}

    def predict_text(self, text):
        text = self.preprocessor(text)
        vectorized = self.vectorizer.transform([text])
        if not vectorized.mean():
            return 'not defined'
        return self.classes_dict[self.model.predict(vectorized)[0]]
    
    @staticmethod
    def preprocessor(text):
        stemmer = PorterStemmer()
        return ' '.join([stemmer.stem(w) for w in re.findall(r'[a-zA-z]*\b',text) if w])