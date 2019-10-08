# -*- coding: utf-8 -*-
__author__ = 'Veselov Andrey'
import time
import pickle
from flask import Flask, render_template, request
import sys

app = Flask(__name__)

print("Preparing classifier")
sys.stdout.flush()
start_time = time.time()

with open('predictor.pickle', 'rb') as f:
  predictor = pickle.load(f)

print("Classifier is ready")
print(time.time() - start_time, "seconds")
sys.stdout.flush()

@app.route("/", methods=["POST", "GET"])
def index_page(text="", prediction_message=""):
    if request.method == "POST":
        text = request.form["text"]
        text_prediction = predictor.predict([text])[0]
	prediction_message = u"Кажется, это позитивный отзыв" if text_prediction==0 else u"Кажется, это негативный отзыв"
    return render_template('index.html', text=text, prediction_message= u"Будет здесь" if len(prediction_message)==0 else prediction_message)

app.run(host='0.0.0.0', port=8000, debug=False)
