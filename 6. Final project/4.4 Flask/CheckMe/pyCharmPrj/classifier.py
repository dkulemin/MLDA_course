import nltk
import pandas as pd
import logging
import re
from nltk.corpus import stopwords as nltk_stop_words
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


lemma = nltk.wordnet.WordNetLemmatizer()
stop_words = set(nltk_stop_words.words("english"))

class Classifier(object):
    def __init__(self, logging_level = logging.DEBUG, console_level=logging.WARNING):
        try:
            nltk_stop_words.words("english")
            nltk.wordnet.WordNetLemmatizer()
        except:
            nltk.download('stopwords') # Если ругнется - загрузим (Мусорные слова)
            nltk.download('wordnet') # Если ругнется - загрузим (Словарь для лемматизации)

        self.classes_dict = {0: "negative", 1: "positive", -1: "prediction error"}
        self.logger = self.function_logger(logging_level, console_level)
        self.model = self.create_model()

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

    @staticmethod
    def clear_string(text): # Преобразование строки перед predict-ом
        strs = text.lower()  # Переводим в нижний регистр
        strs = re.sub('>', '> ', strs)  # Закрывающий html тэг завершаем пробелом
        strs = re.sub('<[^<]+?>', '', strs)  # Убираем xml/html тэги
        strs = re.sub('[^\w\s]', '', strs)  # Убираем знаки препинания
        strs = re.sub(' +', ' ', strs)  # Заменяем двойные+ пробелы на одинарные
        strs = re.sub('\d', '', strs)  # Удаляем цифры
        s_list = nltk.word_tokenize(strs) # Переводим строку в массив слов
        s_list = [item for item in s_list if item not in stop_words] # Удаляем стоповые слова
        s_list = [lemma.lemmatize(item) for item in s_list] # Приводим к норм словоформе
        return  " ".join(s_list) # Собираем обратно массив слов в строку

    @staticmethod
    def function_logger(file_level, console_level=None): # Сделаем правильно логгер
        function_name = "classifier"
        logger = logging.getLogger(function_name)
        logger.setLevel(logging.DEBUG)

        if console_level is not None: # Если указали дубляж логов на консоль
            ch = logging.StreamHandler()
            ch.setLevel(console_level)
            ch_format = logging.Formatter('%(asctime)s - %(message)s')
            ch.setFormatter(ch_format)
            logger.addHandler(ch)

        print("filename" + "{0}.log".format(function_name))
        fh = logging.FileHandler("{0}.log".format(function_name))
        fh.setLevel(file_level)
        fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
        fh.setFormatter(fh_format)
        logger.addHandler(fh)
        return logger

    def prepare_df(self):
        df_train = pd.read_csv("labeledTrainData.csv", sep="\t")  # 18000 отзывов на фильмы из базы imdb
        self.logger.warning("train data loaded")
        return df_train

    def create_model(self):  # Построим модель (параметры подобрал заранее по сетке)
        df = self.prepare_df()
        pipe = Pipeline([('tfidf', TfidfVectorizer(max_df=0.15, ngram_range=(1, 2))),
                         ('lr', LogisticRegression(C=250))])
        pipe.fit(df.processed_text, df.sentiment)
        self.logger.warning("model created")
        return pipe

    def predict_text(self, text):  # Определение тональности отзыва
        pred_type, p_value = -1, 0.8
        try:
            st = self.clear_string(text)
            print("st", st)
            print(self.model.predict([st]))
            pred_type = self.model.predict([st])[0]
            p_value = self.model.predict_proba([st])[0][pred_type]
            return pred_type, p_value
        except:
            self.logger.error("prediction error")
        return pred_type, p_value

    def predict_list(self, list_of_texts):
        try:
            return self.model.predict(list_of_texts), self.model.predict_proba(list_of_texts)
        except:
            self.logger.error("prediction error")
            return None

    def get_prediction_message(self, text):
        prediction = self.predict_text(text)
        class_prediction = prediction[0]
        prediction_probability = prediction[1]
        return self.get_probability_words(prediction_probability) + " " + self.classes_dict[class_prediction]

