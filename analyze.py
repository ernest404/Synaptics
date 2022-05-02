import fitz #pymupdf library
import extract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

path = "uploads/news.pdf"


def highlighter(path):

        # read pdf    
        pdf = fitz.open(path)

        #create list of all pages to iterate through
        def createList(r2):
                return [i for i in range(1, r2)]
        s = createList(pdf.page_count)

        # get trigger-words used in extract module
        triggerwords = extract.triggerwords
        for i in s:
                page = pdf[i]    
                # search for trigger-words in pages  
                text_instances = [page.search_for(triggerword) for triggerword in triggerwords]    
                # hightlight    
                for inst in text_instances:
                        highlight = page.add_highlight_annot(inst)  

        # output    
        return pdf.save("uploads/news1.pdf", garbage=4, deflate=True, clean=True)

def listToString(s):
        # initialize an empty string
        str1 = " "
        # return string
        return (str1.join(s))

def remove_stopwords(text):
        stop_words = set(stopwords.words('english'))
        new_stopwords = ['said', 'say,', 'make', 'added', 'PeopleDailyKe', 'According', '@PeopleDailyKe', 'one', 'time', 'must']
        stop_words = stop_words.union(new_stopwords)

        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        filtered_sentence = []
        for w in word_tokens:
                if w not in stop_words:
                        filtered_sentence.append(w)
        return listToString(filtered_sentence)



# Function to generate wordcloud
def wordcloudgen(text):
    text = remove_stopwords(text)
    wordcloud = WordCloud ( background_color = 'white', width = 512, height = 384 ).generate(text)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('static/images/World_Cloud.png')
    return 'static/images/World_Cloud.png'

      