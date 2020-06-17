#Used PyPDF2 to take PDF and turn into text document
from nltk.text import Text
import nltk
import re
from nltk.corpus import stopwords

####Initialization####
stopwords = list(stopwords.words("english"))
raw = open("C:/Users/micha/Documents/Python/AI/NLP/Six-Sigma-Green-Belt-Book-Searcher/LSSGBCTM.txt", 'rb').read()
book = {}
raw = raw.decode("utf-8")
raw = raw.replace("\\n","")
tokens = nltk.word_tokenize(raw)
text = nltk.Text(tokens)

####Gathering Chapter Data####
for i in range(24):
    if i == 23:
        start = raw.find("Chapter " + str(i+1) + ":")
        end = len(raw)+1
    else:
        start = raw.find("Chapter " + str(i+1) + ":")
        end = raw.find("Chapter " + str(i+2) + ":")
    tokenIndex = nltk.word_tokenize(raw[start:end])
    end = len(tokenIndex)
    if i == 0:
        cend = end
    else:
        cend = end + book["Chapter"+str(i)]["Index"]
    book["Chapter" + str(i+1)] = {"Index": cend, "Hits":0}

####Defining Search Function####
def search(query):
    searchable = {}
    for word in query:
        word = re.sub('[^a-zA-z0-9]','',word)
        if word.lower() in stopwords:
            continue
        else:
            concordi = text.concordance_list(word)
            positions = []
            for concordance in concordi:
                positions.append(concordance.offset)
            searchable[word] = {"Offsets": positions}
    for word in searchable:
        for offset in searchable[word]["Offsets"]:
            for chapter in book:
                if offset <= book[chapter]["Index"]:
                    book[chapter]["Hits"] += 1
                    break
    bookSort = sorted(book,key=lambda x: (book[x]["Hits"]), reverse=True)
    topChapter = bookSort[0]
    mostHits = book[topChapter]["Hits"]
    if mostHits == 0:
        print("Hmm..didn't seem to find that anywhere..")
    else:
        print(topChapter + " had the most hits with " + str(mostHits) + ". Maybe start looking there?")

####Interactive Chat####
query = input("What words are you looking for?\n").split(" ")
search(query)
cont = True
while cont:
    cont = input("Would you like to search more? (y or n)\n")
    if cont == "n":
        break
    for chapter in book:
        book[chapter]["Hits"] = 0
    query = input("What words?\n").split(" ")
    search(query)