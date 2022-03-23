#!/usr/bin/env python3
from flask import Flask, render_template
from flask import request, redirect, url_for
from werkzeug import secure_filename
import nltk
import lex_rank
import os
import extract
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

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
    # Request file to summarize
    uploaded_file  = request.files['filename']
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], "news.pdf"))
    
    articles = extract.extract_articles("uploads/news.pdf")
    # Request number of senetences to summarize to
    n_sentences = int(request.form.get("sentences"))

    # news =  send_from_directory(app.config['UPLOAD_FOLDER'], f.filename)
    # Invoke lexical summarizer 
    lr = lex_rank.LexRankSummarizer(n_sentences)

    summary_list = []
    for article in articles:
        summary_list.append(lr(article))
    
    # Remove any duplicates from the list
    summary_list = list(dict.fromkeys(summary_list))
    return render_template("summarize.html", filename=uploaded_file.filename, summary_list = summary_list)

if __name__ == "__main__":
    nltk.download('stopwords')
    nltk.download('punkt')
    # app.run(host="0.0.0.0")
    app.run(debug = True)

####
import os

fileitem = form['filename']

# check if the file has been uploaded
if fileitem.filename:
	# strip the leading path from the file name
	fn = os.path.basename(fileitem.filename)
	
# open read and write the file into the server
	open(fn, 'wb').write(fileitem.file.read())
