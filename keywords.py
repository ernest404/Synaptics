# Importing Libraries
from nltk import tokenize
from operator import itemgetter
import math

# TF (Term Frequency) = Number of times a term t appears in the text / Total number of words in the document
# IDF (Inverse Document Frequency) = log(total number of sentences / Number of sentences with term t)
# TF-IDF = TF * IDF = More TF-IDF value, more important is the variable

# Document -> Vectorize -> Find TF -> Find IDF -> Find TF*IDF -> Keywords

# Document text
doc = '''- Xinhua
A rebel attack on an army base in 
central Mali on Friday has killed at 
least 27 soldiers and wounded 33 more, 
the government said, adding that at 
least seven soldiers are still missing 
following the complex attack in the 
rural commune of Mondoro, which in-
volved car bombs. Seventy “terrorists” 
were killed in the military’s response, 
the statement said on Friday, without 
specifying which armed group was 
responsible. Afﬁliates of both al-Qaeda 
and ISIL (ISIS) are active in central 
Mali. The Mondoro base is near Mali’s 
border with Burkina Faso and has pre-
viously been targeted by rebels ﬁghting 
the Malian state and foreign forces.  
About 50 soldiers died after an attack 
on Mondoro and the nearby Boulkessi 
camp in September 2019.  '''
#doc = 'Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly, procedural), object-oriented, and functional programming. Python is often described as a "batteries included" language due to its comprehensive standard library. Python was created in the late 1980s, and first released in 1991, by Guido van Rossum as a successor to the ABC programming language.'

# Remove stopwords
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
stop_words = set(stopwords.words('english')) 

# Step 1 : Find total words in the document
total_words = doc.split()
total_word_length = len(total_words)
# print(total_word_length)
#28

# Step 2 : Find total number of sentences
total_sentences = tokenize.sent_tokenize(doc)
total_sent_len = len(total_sentences)
# print(total_sent_len)
#7

# Step 3: Calculate TF for each word
tf_score = {}
for each_word in total_words:
    each_word = each_word.replace('.','')
    if each_word not in stop_words:
        if each_word in tf_score:
            tf_score[each_word] += 1
        else:
            tf_score[each_word] = 1
# print(tf_score)

# Dividing by total_word_length for each dictionary element
tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())

# print(tf_score)

# {'Python': 4, 'increases': 1, 'interesting': 1, 'time': 1, 'graduate': 1, 'thinking': 1, 'want': 1, 'learning': 2, 'Learning': 1, 'Everyone': 1, 'invest': 1, 'I': 3, 'learn': 1, 'like': 1, 'easy': 1}
# {'Python': 0.14285714285714285, 'increases': 0.03571428571428571, 'interesting': 0.03571428571428571, 'time': 0.03571428571428571, 'graduate': 0.03571428571428571, 'thinking': 0.03571428571428571, 'want': 0.03571428571428571, 'learning': 0.07142857142857142, 'Learning': 0.03571428571428571, 'Everyone': 0.03571428571428571, 'invest': 0.03571428571428571, 'I': 0.10714285714285714, 'learn': 0.03571428571428571, 'like': 0.03571428571428571, 'easy': 0.03571428571428571}

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

# Performing a log and divide
idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

# print(idf_score)

# {'Python': 0.5596157879354227, 'increases': 1.9459101490553132, 'interesting': 1.9459101490553132, 'time': 1.9459101490553132, 'graduate': 1.9459101490553132, 'thinking': 1.9459101490553132, 'want': 1.9459101490553132, 'learning': 1.252762968495368, 'Learning': 1.9459101490553132, 'Everyone': 1.9459101490553132, 'invest': 1.9459101490553132, 'I': 0.8472978603872037, 'learn': 1.9459101490553132, 'like': 1.9459101490553132, 'easy': 1.9459101490553132}

# Step 5: Calculating TF*IDF
tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()} 
# print(tf_idf_score)

# {'Python': 0.07994511256220323, 'increases': 0.06949679103768976, 'interesting': 0.06949679103768976, 'graduate': 0.06949679103768976, 'time': 0.06949679103768976, 'want': 0.06949679103768976, 'learning': 0.08948306917824057, 'like': 0.06949679103768976, 'Everyone': 0.06949679103768976, 'invest': 0.06949679103768976, 'I': 0.09078191361291467, 'thinking': 0.06949679103768976, 'learn': 0.06949679103768976, 'Learning': 0.06949679103768976, 'easy': 0.06949679103768976}

# Get top N important words in the document
def get_top_n(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
    return result

print(get_top_n(tf_idf_score, 10))

# {'Python': 0.07994511256220323, 'learning': 0.08948306917824057, 'I': 0.09078191361291467, 'interesting': 0.06949679103768976, 'increases': 0.06949679103768976}

