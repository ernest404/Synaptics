#!/usr/bin/env python3
from flask import Flask, render_template
from flask import request
import nltk
import lex_rank

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze")
def analyze():
    return render_template("analyze.html")

@app.route("/summarize")
def summarize():
    return render_template('summarize.html')

@app.route("/submit", methods=["POST"])
def submit():
    # Request text to summarize
    text = request.form.get("text")

    # Request summarization parameters
    n_sentences = int(request.form.get("sentences"))

    # Invoke lexical summarizer 
    lr = lex_rank.LexRankSummarizer(n_sentences)
    summary = lr(text)

    return render_template("summarize.html", text=text, summary=summary)

if __name__ == "__main__":
    nltk.download('stopwords')
    nltk.download('punkt')
    # app.run(host="0.0.0.0")
    app.run(debug = True)

