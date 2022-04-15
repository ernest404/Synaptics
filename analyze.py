import fitz
import extract
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

# highlight(path)

def wordcloudgen(text):

    wordcloud = WordCloud ( background_color = 'white', width = 512, height = 384 ).generate(text)
    
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('static/images/World_Cloud.png')
    return 'static/images/World_Cloud.png'

      