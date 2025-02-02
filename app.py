from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from summarize import summarize
from gap_questions import create_gap_questions
import json
from flask_cors import CORS

import random
import math

# App config.
DEBUG = True
app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class QuizGenerator(Form):
    topic = TextField('Topic:')
    article = TextField('Article:', validators=[validators.required(), validators.Length(min=100, message=(u'Must be atleast 100 words length'))])
    
    @app.route("/", methods=['POST'])
    def hello():
        data = json.loads(request.data)
        article = data['article']
        # print(data)

        summarized_text, summary_sentences = summarize(article)

        gap_questions = []

        for sentence in summary_sentences:
            gap_question = create_gap_questions(sentence)
            if gap_question:
                gap_questions.append(gap_question)

        # print(gap_questions)
        return (json.dumps(gap_questions), 200)

    @app.route("/summary", methods=['POST'])
    def generateSummary():
        data = json.loads(request.data)
        article = data['article']

        summarized_text, summary_sentences = summarize(article)

        return (json.dumps(summarized_text), 200)

if __name__ == "__main__":
    app.run()