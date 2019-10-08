from sentiment_classifier import SentimentClassifier
from codecs import open
import time
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import spacy
from string import punctuation
import nltk
nltk.download("stopwords")

app = Flask(__name__)
bootstrap = Bootstrap(app)

print("Подготовка классификатора")
start_time = time.time()
russian_stopwords = nltk.corpus.stopwords.words('russian')
nlp = spacy.load('ru2', disable=["parser", "ner"])
classifier = SentimentClassifier()
print("Классификатор готов")
print(time.time() - start_time, "секунд")


@app.route("/sentiment-demo", methods=["POST", "GET"])
def index_page(text="", prediction_message=""):
    if request.method == "POST":
        text = request.form["text"]
        logfile = open("ydf_demo_logs.txt", "a", "utf-8")
        print(text)
        print("<response>", file=logfile)
        print(text, file=logfile)
        prediction_message = classifier.get_prediction_message(text)
        print(prediction_message)
        print(prediction_message, file=logfile)
        print("</response>", file=logfile)
        logfile.close()

    return render_template('base.html', text=text, prediction_message=prediction_message)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
