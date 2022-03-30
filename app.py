#!/usr/bin/env python3
from flask import Flask, render_template
from flask import request, make_response,redirect, url_for
import pdfkit 
import lex_rank
import os
import extract
import nltk

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/analyze")
def analyze():
    return render_template("analyze.html")

@app.route("/summarize")
def summarize():
    return render_template('summarize.html')

@app.route("/submit", methods=["POST"])
def submit():
    # Request file to summarize
    uploaded_file  = request.files['filename']
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], "news.pdf"))
    
    articles = extract.extract_articles("uploads/news.pdf")

    # Request number of senetences to summarize to
    n_sentences = int(request.form.get("sentences"))

    # Invoke lexical summarizer 
    lr = lex_rank.LexRankSummarizer(n_sentences)

    global summary_list 
    summary_list = []
    for article in articles:
        summary_list.append(lr(article))
    
    # Remove any duplicates from the list
    summary_list = list(dict.fromkeys(summary_list))
   
    return render_template("summarize.html", filename=uploaded_file.filename, summary_list = summary_list)

@app.route("/pdf")
def pdf():
    html = render_template("summary.html", summary_list = summary_list)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=summary.pdf"
    return response



if __name__ == "__main__":
  
    # app.run(host="0.0.0.0")
    nltk.download('stopwords')
    app.run(debug = True)
