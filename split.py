import fitz

def createList(r2):
    return [i for i in range(1, r2)]

pdf = fitz.open('news.pdf')
s = createList(pdf.page_count)

print(pdf.metadata)

text_by_page = [pdf.get_page_text(i) for i in s]


keywords = ["Kenya Defence Forces", "KDF", "Military", "Army", "Airforce", "Navy", "National Security", "Security", "Terrorism", "AlShabaab"]

for page in text_by_page:
    for keyword in keywords:
        if keyword.lower() in page.lower():
         print(page.metadata['keywords'])