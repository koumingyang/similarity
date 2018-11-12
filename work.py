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

texts = []
texts_xls = [[]]

author_project_id = [-1]
author_cnt = 0

all_authors = []
all_projects = [[]]
all_dict = []
all_json = []
json_cnt = 0

def init(string):
    texts_tokenized = [word.lower() for word in word_tokenize(string)]
    texts_filtered = [st.stem(word) for word in texts_tokenized if (not word in english_stopwords) and (not word in english_punctuations)]
    return texts_filtered

def deal_json(json_string):
    json_dict = json.loads(json_string)
    if json_dict["abstract"] == "":
        return

    id = (int)(json_dict["id"])
    author_id = author_project_id[id]
    title = json_dict["title"].lower()

    for one_title in all_authors[author_id]["titles"]:
        if title == one_title:
            return

    flag = False
    school_xls = all_authors[author_id]["school"]
    for org in json_dict["org"]:
        try:
            school_json = org.lower()
            if (school_json in school_xls) or (school_xls in school_json): 
                flag = True
                break
        except:
            pass
    if flag == False:
        return

    all_authors[author_id]["titles"].append(title)

    global json_cnt
    json_cnt += 1
    if json_cnt % 1000 == 0:
        print(".json dealed", json_cnt)

    new_json_dict = {}
    new_json_dict["researcher_name_in_nsf_list"] = json_dict["ori_name"]
    new_json_dict["researcher_paper_title_in_json_file"] = json_dict["title"]
    new_json_dict["researcher_paper_abstract_in_json_file"] = json_dict["abstract"]
    new_json_dict["paper_keywords"] = json_dict["keywords"]
    new_json_dict["paper_citation"] = json_dict["citation"]
    new_json_dict["year"] = json_dict["year"]
    new_json_dict["field"] = json_dict["feild"]
    new_json_dict["researcher_nsf_project_abstract"] = []
    new_json_dict["researcher_id"] = []
    new_json_dict["score_lsi"] = []
    new_json_dict["score_lda"] = []
    new_json_dict["projects_cnt"] = all_authors[author_id]["projects"]

    for project_id in all_authors[author_id]["id"]:
        new_json_dict["researcher_id"].append(project_id)
        new_json_dict["researcher_nsf_project_abstract"].append(texts_xls[project_id])
    
    all_json.append(new_json_dict)

def deal_string(json_dict, lsi, index_lsi, lda, index_lda):
    abs_str = json_dict["researcher_paper_abstract_in_json_file"]
    year = (int)(json_dict["year"])
    abs_dict = init(abs_str)
    abs_corpus = dictionary.doc2bow(abs_dict)
    
    query_lsi = lsi[abs_corpus]
    sims_lsi = index_lsi[query_lsi]
    abs_sims_lsi = list(enumerate(sims_lsi))
    query_lda = lda[abs_corpus]
    sims_lda = index_lda[query_lda]
    abs_sims_lda = list(enumerate(sims_lda))

    for iid in json_dict["researcher_id"]:
        id = (int)(iid)
        abs_sim_lsi = abs_sims_lsi[(int)(id)]
        lsi_score = abs_sim_lsi[1]
        json_dict["score_lsi"].append((str)(lsi_score))
        abs_sim_lda = abs_sims_lda[(int)(id)]
        lda_score = abs_sim_lda[1]
        json_dict["score_lda"].append((str)(lda_score))

        if year >= 2015 and year <= 2017:
            all_projects[id]["lsi_score_after_2015"].append(lsi_score)
            all_projects[id]["lda_score_after_2015"].append(lda_score)
            all_projects[id]["paper_numbers_after_2015"] += 1
            all_projects[id]["max_lsi_score_after_2015"] = max(all_projects[id]["max_lsi_score_after_2015"], lsi_score)
            all_projects[id]["max_lda_score_after_2015"] = max(all_projects[id]["max_lda_score_after_2015"], lda_score)
        else:
            all_projects[id]["lsi_score_before_2015"].append(lsi_score)
            all_projects[id]["lda_score_before_2015"].append(lda_score)
            all_projects[id]["paper_numbers_before_2015"] += 1
            all_projects[id]["max_lsi_score_before_2015"] = max(all_projects[id]["max_lsi_score_before_2015"], lsi_score)
            all_projects[id]["max_lda_score_before_2015"] = max(all_projects[id]["max_lda_score_before_2015"], lda_score)

        all_projects[id]["max_lsi_score"] = max(all_projects[id]["max_lsi_score"], lsi_score)
        all_projects[id]["max_lda_score"] = max(all_projects[id]["max_lda_score"], lda_score)
        all_projects[id]["min_lsi_score"] = min(all_projects[id]["min_lsi_score"], lsi_score)
        all_projects[id]["min_lda_score"] = min(all_projects[id]["min_lda_score"], lda_score)
        all_projects[id]["paper_numbers_all"] += 1

    new_string = json.dumps(json_dict)
    with open("info_all_papers.json", 'a', encoding='utf-8') as fo:
        fo.write(new_string)
        fo.write("\n")

workbook = xlrd.open_workbook('exportAwards-2015.xls')  
#print(workbook.sheet_names())                  #查看所有sheet  
booksheet = workbook.sheet_by_index(0)         #用索引取第一个sheet  

for i in range(1, 13905):
    abs_str = booksheet.cell(i, 40).value
    name_str = booksheet.cell(i, 2).value
    school_str = (booksheet.cell(i, 32).value).lower()
    flag = False

    for j in range(author_cnt):
        if name_str == all_authors[j]["name"] and school_str == all_authors[j]["school"]:
            all_authors[j]["id"].append(i)
            all_authors[j]["projects"] += 1
            author_project_id.append(j)
            flag = True
            break
    if flag == False:
        new_author = {}
        new_author["name"] = name_str
        new_author["school"] = school_str
        new_author["id"] = []
        new_author["id"].append(i)
        new_author["titles"] = []
        new_author["projects"] = 1
        author_project_id.append(author_cnt)
        all_authors.append(new_author)
        author_cnt += 1

    texts_xls.append(abs_str)

    author_dict = {}
    author_dict["researcher_name"] = booksheet.cell(i, 2).value
    author_dict["researcher_id"] = i
    author_dict["lsi_score_after_2015"] = []
    author_dict["lsi_score_before_2015"] = []
    author_dict["lda_score_after_2015"] = []
    author_dict["lda_score_before_2015"] = []
    author_dict["max_lsi_score"] = 0.0
    author_dict["max_lda_score"] = 0.0
    author_dict["max_lsi_score_after_2015"] = 0.0
    author_dict["max_lda_score_after_2015"] = 0.0
    author_dict["max_lsi_score_before_2015"] = 0.0
    author_dict["max_lda_score_before_2015"] = 0.0
    author_dict["min_lsi_score"] = 1.0
    author_dict["min_lda_score"] = 1.0
    author_dict["paper_numbers_after_2015"] = 0
    author_dict["paper_numbers_before_2015"] = 0
    author_dict["paper_numbers_all"] = 0
    all_projects.append(author_dict)

    if i % 500 == 0:
        print("nsf .xls dealed", i, "authors", author_cnt)

print("authors numbers", author_cnt)

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

cnt = 0
with open('clear_texts_151617.txt', encoding='utf-8') as f:
    for line in f:
        texts.append(line.split(' '))
        cnt += 1
        if cnt % 100000 == 0:
            print("clear txt read", cnt)
print("------------------------summarize finished----------------------------")

dictionary = corpora.Dictionary(texts)
print("-------------------------dictionary built-----------------------------")

print(texts[1])

corpus = [dictionary.doc2bow(text) for text in texts]
print("---------------------------corpus get---------------------------------")
tfidf = models.TfidfModel(corpus)
print("-----------------------tfidf model build over-------------------------")
corpus_tfidf = tfidf[corpus]
print("------------------------tfidf corpus get------------------------------")

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=50)
print("----------------------lsi/lda model build over-------------------------")
index_lsi = similarities.MatrixSimilarity(lsi[corpus])
index_lda = similarities.MatrixSimilarity(lda[corpus])
print("----------------------lsi/lda index build over--------------------------")

cnt = 0
for json_dict in all_json:
    deal_string(json_dict, lsi, index_lsi, lda, index_lda)
    cnt += 1
    if cnt % 100 == 0:
        print("json dict dealed", cnt)

author_cnt = 0
with open('info_all_projects.json', 'w', encoding='utf-8') as fo:
    for i in range(13905):
        new_dict = all_projects[i]
        if not i == 0:
            cnt = (int)(new_dict["paper_numbers_all"])
            print(cnt)
            if cnt > 0 and cnt <= 200:
                author_cnt += 1
                new_string = json.dumps(dict_authors[i])
                fo.write(new_string)
                fo.write("\n")
                if author_cnt % 2000 == 0:
                    print("author json outputed", i)

print("all authors", author_cnt)
