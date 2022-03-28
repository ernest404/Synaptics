import fitz
import keywords


def extract_articles(path):
    pdf = fitz.open(path)

    def createList(r2):
        return [i for i in range(1, r2)]

    s = createList(pdf.page_count)

    text_by_page = [(pdf.load_page(i)).get_text("text") for i in s]

    # text_by_page = [pdf.get_page_text(i) for i in s]

    x = [i for i in range(0, pdf.page_count-1)]
   
    triggerwords = ["Kenya Defence Forces", "KDF", "Military", "Army", "Airforce", "Navy", "National Security", "Security", "Terrorism", "Terror","Terrorist",
                "AlShabaab","Al-Shabaab","Al Shabaab", "bandits", "gunshot", "gun", "firearm", "bomb", "bombing", "bombed", "Taliban","Department of Defence", 
                "militia", "threat", "Al Qaeda", "weapons", "bomber", "extremist", "extremism", "pirates"]

    filtered_articles = []
    for i in x:
        text_by_page[i] = text_by_page[i].replace('\n', '')
        text_by_page[i] = text_by_page[i].replace('-', '')
        text_by_page[i] = text_by_page[i].replace('�', '')
        text_by_page[i] = text_by_page[i].replace('  ', '\n')
        text_by_page[i] = text_by_page[i].replace('@PeopleDailyKe', '\n\n')
        text_by_page[i] = text_by_page[i].split('\n\n')

        for j in text_by_page[i]:
            keyword = keywords.extract_keywords(j)
            for triggerword in triggerwords:
                if triggerword.lower() in [x.lower() for x in keyword]:
                    filtered_articles.append(j)
                    # print(j + '\n\n')
    return filtered_articles