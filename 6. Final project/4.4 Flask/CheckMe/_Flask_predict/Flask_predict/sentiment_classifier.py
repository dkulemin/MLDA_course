__author__ = 'Maksimov Andrey'

from sklearn.externals import joblib


class SentimentClassifier(object):
    def __init__(self):
        self.model = joblib.load("./model_for_predict.pkl")
        #self.vectorizer = joblib.load("./BigramUnprocessedVectorizer.pkl")
        self.classes_dict = {0: u"Отрицательный", 1: u"Положительный", -1: u"Ошибка"}

    @staticmethod
    def get_probability_words(probability):
        if probability < 0.55:
            return "neutral or uncertain"
        if probability < 0.7:
            return "probably"
        if probability > 0.95:
            return "certain"
        else:
            return ""

    def predict_text(self, text):
        try:
            return self.model.predict([text])[0]
        except:
            print ("Ошибка в тексте")
            return -1, 0.8



    def get_prediction_message(self, text):
        prediction = self.predict_text(text)
        class_prediction = prediction
        return  u"Отзыв: " + self.classes_dict[class_prediction]