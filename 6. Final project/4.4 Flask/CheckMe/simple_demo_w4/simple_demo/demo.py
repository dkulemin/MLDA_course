from sentiment_classifier import SentimentClassifier
from codecs import open
import time
from flask import Flask, render_template, request
app = Flask(__name__)

print("Preparing classifier")
start_time = time.time()
classifier = SentimentClassifier()
print("Classifier is ready")
print(time.time() - start_time, "seconds")

@app.route("/", methods=["POST", "GET"])
def index_page():
    text = None
    if request.method == "POST":
        text = request.form["text"]
        logfile = open("demo_logs.txt", "a", "utf-8")
        prediction_message = classifier.predict_text(text)
        print(f"'{text}': predict score - {prediction_message}", end='\r\n', file=logfile)
        logfile.close()
    if text is None:
        return render_template('hello.html')
    else:
        return render_template('hello.html', text=text, prediction_message=prediction_message)


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=False)
