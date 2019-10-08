from sklearn.externals import joblib


class SentimentClassifier(object):
    def __init__(self):
        self.model = joblib.load("./LemmatizedTfidfLinearSVCTextSentiment.pkl")
        self.classes_dict = {0: "негативный", 1: "позитивный", -1: "ошибка предсказания"}

    @staticmethod
    def get_probability_words(probability):
        if probability < 0.55:
            return "нейтральный или неуверенно"
        if probability < 0.7:
            return "возможно"
        if probability > 0.95:
            return "определенно"
        else:
            return ""

    def predict_text(self, text):
        try:
            return self.model.predict([text])[0],\
                   self.model.predict_proba([text])[0].max()
        except:
            print('ошибка предсказания')
            return -1, 0.8

    def predict_list(self, list_of_texts):
        try:
            return self.model.predict(list_of_texts),\
                   self.model.predict_proba(list_of_texts)
        except:
            print('ошибка предсказания')
            return None

    def get_prediction_message(self, text):
        prediction = self.predict_text(text)
        class_prediction = prediction[0]
        prediction_probability = prediction[1]
        return self.get_probability_words(prediction_probability) + " " + self.classes_dict[class_prediction]