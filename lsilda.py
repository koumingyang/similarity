import xlrd
import json
import nltk
import gensim
import sys
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

texts_paper = []
texts_corpus = []
texts_project = []

lsi_all = []
lda_all = []

def init(string):
    texts_tokenized = [word.lower() for word in word_tokenize(string)]
    texts_filtered = [st.stem(word) for word in texts_tokenized if (not word in english_stopwords) and (not word in english_punctuations)]
    return texts_filtered

def deal_string(abs_str, lsi, index_lsi, lda, index_lda):
    abs_dict = init(abs_str)
    abs_corpus = dictionary.doc2bow(abs_dict)
    
    query_lsi = lsi[abs_corpus]
    sims_lsi = index_lsi[query_lsi]
    abs_sims_lsi = list(enumerate(sims_lsi))
    query_lda = lda[abs_corpus]
    sims_lda = index_lda[query_lda]
    abs_sims_lda = list(enumerate(sims_lda))
    return abs_sims_lsi, abs_sims_lda

filename_corpus = sys.argv[1]
filename_paper = sys.argv[2]
filename_project = sys.argv[3]

print(filename_corpus, filename_paper, filename_project)

with open(filename_corpus, encoding='utf-8') as f:
    for line in f:
        texts_corpus.append(line.split(' '))

paper_cnt = 0
with open(filename_paper, encoding='utf-8') as f:
    for line in f:
        paper_cnt += 1
        texts_paper.append(line.split(' '))

project_cnt = 0
with open(filename_project, encoding='utf-8') as f:
    for line in f:
        project_cnt += 1
        texts_project.append(line)

dictionary = corpora.Dictionary(texts_corpus)
corpus = [dictionary.doc2bow(text) for text in texts_corpus]
paper = [dictionary.doc2bow(text) for text in texts_paper]
print("---------------------------corpus get---------------------------------")
tfidf = models.TfidfModel(corpus)
print("-----------------------tfidf model build over-------------------------")
corpus_tfidf = tfidf[corpus]
print("------------------------tfidf corpus get------------------------------")
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=50)
print("----------------------lsi/lda model build over-------------------------")
index_lsi = similarities.MatrixSimilarity(lsi[paper])
index_lda = similarities.MatrixSimilarity(lda[paper])

for text_project in texts_project:
    lsi_one, lda_one = deal_string(text_project, lsi, index_lsi, lda, index_lda)
    lsi_all.append(lsi_one)
    lda_all.append(lda_one)

with open('lsi.txt', 'w', encoding='utf-8') as fo:
    fo.write("Papers: " + (str)(paper_cnt) + " Projects: " + (str)(project_cnt)+ "\n")
    for line in lsi_all:
        for one in line: 
            fo.write((str)(one[1]))
            fo.write("\t")
        fo.write("\n")

with open('lda.txt', 'w', encoding='utf-8') as fo:
    fo.write("Papers: " + (str)(paper_cnt) + " Projects: " + (str)(project_cnt) + "\n")
    for line in lda_all:
        for one in line: 
            fo.write((str)(one[1]))
            fo.write("\t")
        fo.write("\n")

