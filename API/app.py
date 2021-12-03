import logging
import os
import re
from threading import Thread
from flask import Flask, render_template, jsonify
from flask import request, redirect, url_for, flash
from requests.api import delete

import classifiedModel
import generatedModel

app = Flask(__name__)


@app.route('/api/model/classify', methods=["GET", "POST"])
def classify():
    if request.method == "POST":

        text = request.json["text"]
        r = classifiedModel.predict(text)

        return {
            "result": r
        }


    return "<h1>Classified Model</h1>"

@app.route('/api/model/generate', methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        text = request.json["text"]
        diversity = request.json["diversity"]
        r = generatedModel.predict_post(text, diversity)

        return {
            "result": r
        }

    results = generatedModel.predict_get()
    return {
        "toxic tweet" : results[0],
        "not toxic tweet" : results[1]
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6060)
