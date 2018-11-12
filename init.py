import xlrd
import json
import nltk
import gensim
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from gensim import corpora, models, similarities
import logging
import http.client, urllib.request, urllib.parse, urllib.error, base64

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
st = LancasterStemmer()
english_stopwords = stopwords.words('english')
english_punctuations = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', 
'+', '{', '}', '[', ']', '\\', '|', ';', ':', '\'', '\"', ',', '.', '/', '<', '>', '?']

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'a980594293614d9d8660253b9b8691d0',
}

texts_stemmed = [[]]
texts_xls = [[]]
all_dict = []
all_json = []
json_cnt = 0

def init(string):
    s = ""
    for ch in string:
        if ch >= '\0' and ch <= chr(127):
            s += ch
    texts_tokenized = [word.lower() for word in word_tokenize(string)]
    texts_filtered = [st.stem(word) for word in texts_tokenized if (not word in english_stopwords) and (not word in english_punctuations)]
    return texts_filtered

def deal_json(json_string):
    json_dict = json.loads(json_string)
    if json_dict["abstract"] == "":
        return
    if (not ((int)(json_dict["year"]) == 2017)) and (not ((int)(json_dict["year"]) == 2016)) and (not ((int)(json_dict["year"]) == 2015)):
        return

    global json_cnt
    json_cnt += 1
    if json_cnt % 1000 == 0:
        print(".json dealed", json_cnt)

    all_json.append(json_dict)
    abs_str = json_dict["abstract"]
    abs_dict = init(abs_str)
    texts_stemmed.append(abs_dict)

def deal_string(json_dict, lsi, index_lsi, lda, index_lda):
    if json_dict["abstract"] == "":
        return

    id = (int)(json_dict["id"])
    #print(id)
    abs_str = json_dict["abstract"]
    abs_dict = init(abs_str)
    abs_corpus = dictionary.doc2bow(abs_dict)
    
    query_lsi = lsi[abs_corpus]
    sims = index_lsi[query_lsi]
    abs_sim = list(enumerate(sims))[(int)(id)]
    json_dict["simi_score_lsi"] = (str)(abs_sim[1])
    query_lda = lda[abs_corpus]
    sims = index_lda[query_lda]
    abs_sim = list(enumerate(sims))[(int)(id)]
    json_dict["simi_score_lda"] = (str)(abs_sim[1])

    #print(json_dict["simi_score_lsi"], json_dict["simi_score_lda"])

    new_string = json.dumps(json_dict)
    with open("info_clear_simi.json", 'a') as fo:
        fo.write(new_string)
        fo.write("\n")

workbook = xlrd.open_workbook('exportAwards-2015.xls')  
#print(workbook.sheet_names())                  #查看所有sheet  
booksheet = workbook.sheet_by_index(0)         #用索引取第一个sheet  

for i in range(1, 13905):
    abs_str = booksheet.cell(i, 40).value
    abs_dict = init(abs_str)
    texts_xls.append(abs_str)
    texts_stemmed.append(abs_dict)
    if i % 500 == 0:
        print("nsf .xls dealed", i)

json_string = ""
cnt = 0
with open('nsfinfor2015.json', encoding='utf-8') as f:
    for line in f:
        json_string += line
        if (line[0] == '}'):
            deal_json(json_string)
            json_string = ""
            cnt += 1
            if cnt % 100000 == 0:
                print("json file read", cnt)

print(texts_stemmed[36])
print(texts_stemmed[37])
cnt = 0
str_cnt = 0

with open("all_texts_151617.txt", 'w', encoding='utf-8') as ft:
    for one_text in texts_stemmed:
        for one_str in one_text:
            ft.write(one_str)
            ft.write(" ")
            str_cnt += 1
        ft.write("\n")
        cnt += 1
        if cnt % 10000 == 0:
            print("text output", cnt)

print("total line", cnt)
print("total string", str_cnt)