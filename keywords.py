from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk import tokenize
from operator import itemgetter
import math


# TF (Term Frequency) = Number of times a term t appears in the text / Total number of words in the text
# IDF (Inverse Document Frequency) = log(total number of sentences / Number of sentences with term t)
# TF_IDF = TF * IDF = the more TF_IDF value, the more important is the word

# text -> Vectorize -> Find TF -> Find IDF -> Find TF*IDF -> Keywords

# Document text

def extract_keywords(doc):

    # Define stopwords
    stop_words = set(stopwords.words('english')) 

    # Step 1 : Find total words in the article
    total_words = doc.split()
    total_word_length = len(total_words)


    # Step 2 : Find total number of sentences
    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)


    # Step 3: Calculate TF for each word
    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())



    # Check if a word is there in sentence list
    def check_sent(word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))


    # Step 4: Calculate IDF for each word
    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # Performing log and divide
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

    # Step 5: Calculate TF*IDF
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()} 


    # Get top 20 important words in the document
    def get_top_n(dict_elem):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:40]) 
        return result
    keywords = get_top_n(tf_idf_score).keys()
    return keywords

