#!/usr/bin/env python3
from flask import Flask, render_template
from flask import request, make_response,redirect, url_for, send_file
import pdfkit 
import lex_rank
import os
import extract
import nltk
from analyze import highlighter, wordcloudgen
import fitz
import smtplib
from todocx import doc_builder
from datetime import date



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
def submit_summary():
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
    os.remove("uploads/news.pdf")

    # Create a doc report
    doc_builder(summary_list)


    return render_template("summarize.html", filename=uploaded_file.filename, summary_list = summary_list)

@app.route("/submit2", methods=["POST"])
def submit_analysis():
    # Request newspaper to analyze
    uploaded_file  = request.files['filename']
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], "news_analyse.pdf"))
    # Highlight triggerwords on newspaper
    highlighted_newspaper = highlighter("uploads/news_analyse.pdf")

    pdf = fitz.open("uploads/news_analyse.pdf")
    def createList(r2):
        return [i for i in range(1, r2)]

    s = createList(pdf.page_count)

    text_by_page = [(pdf.load_page(i)).get_text("text") for i in s]
    
    # Plot a wordcloud
    url = wordcloudgen((' '.join(text_by_page)))

    os.remove("uploads/news_analyse.pdf")

    return render_template("analyze.html", filename=uploaded_file.filename ,url = url)



@app.route('/download_highlighted_text',methods=["GET","POST"])
def download_pdf(): 
    try:
       path = f'uploads/news1.pdf'
       return send_file(path, attachment_filename='news_highlighted.pdf', as_attachment=True)
       os.remove("uploads/news1.pdf")

    except Exception as e:
        return str(e)


@app.route('/download_report',methods=["GET","POST"])
def download_docx(): 
    try:
       path = f'downloads/summary report.docx'
       return send_file(path, attachment_filename='summary report {}.docx'.format(date.today().strftime("%d-%m-%Y")), as_attachment=True)
       os.remove('downloads/summary report.docx')

    except Exception as e:
        return str(e)


@app.route("/submitcontact", methods=["POST"])
def submitcontact():
    sender_name = request.form.get("name")
    sender_email = request.form.get("email")
    sender_subject = request.form.get("subject")
    sender_message = request.form.get("message")

    reciever_email = 'synapticke@gmail.com'
    reciever_message = "Message recieved"

    server = smtplib.SMTP("smtp.gmail.com", 25)
    server.starttls()
    server.login("synapticke@gmail.com", "Synaptic404")

    try:
        server.sendmail(sender_email, reciever_email, sender_message)         
        print ("Successfully sent email")
    except smtplib.SMTPException:
        print ("Error: unable to send email")

    return render_template("index.html")





if __name__ == "__main__":
  
    # app.run(host="0.0.0.0")
    nltk.download('stopwords')
    nltk.download('punkt')
    app.run(debug = True)
