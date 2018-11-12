import xlrd
import json
import nltk
import gensim
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from gensim import corpora, models, similarities
import logging
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

dict_authors = [[]]
texts_xls = [[]]

workbook = xlrd.open_workbook('exportAwards-2015.xls')  
#print(workbook.sheet_names())                  #查看所有sheet  
booksheet = workbook.sheet_by_index(0)         #用索引取第一个sheet  

for i in range(1, 13905):
    abs_str = booksheet.cell(i, 40).value
    texts_xls.append(abs_str)

    author_dict = {}
    author_dict["researcher_name"] = booksheet.cell(i, 2).value
    author_dict["researcher_id"] = i
    author_dict["lsi_score_after_2015"] = []
    author_dict["lsi_score_before_2015"] = []
    author_dict["min_lsi_score"] = 1.0
    author_dict["max_lsi_score"] = 0.0
    author_dict["max_lsi_score_after_2015"] = 0.0
    author_dict["max_lsi_score_before_2015"] = 0.0
    author_dict["lda_score_after_2015"] = []
    author_dict["lda_score_before_2015"] = []
    author_dict["min_lda_score"] = 1.0
    author_dict["max_lda_score"] = 0.0
    author_dict["max_lda_score_after_2015"] = 0.0
    author_dict["max_lda_score_before_2015"] = 0.0
    author_dict["stv_score_after_2015"] = []
    author_dict["stv_score_before_2015"] = []
    author_dict["min_stv_score"] = 1.0
    author_dict["max_stv_score"] = 0.0
    author_dict["max_stv_score_after_2015"] = 0.0
    author_dict["max_stv_score_before_2015"] = 0.0
    author_dict["paper_numbers_after_2015"] = 0
    author_dict["paper_numbers_before_2015"] = 0
    author_dict["paper_numbers_all"] = 0
    dict_authors.append(author_dict)

    if i % 500 == 0:
        print("nsf .xls dealed", i)

cnt = 0

embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/1")

with open('info_stv_papers_2015.json', 'w', encoding='utf-8') as fo:
    pass

with open('info_all_papers_2015.json', encoding='utf-8') as f: 
    for line in f:
        json_dict = json.loads(line)
        ids = json_dict["researcher_id"]
        score_lsi_list = json_dict["score_lsi"]
        score_lda_list = json_dict["score_lda"]
        year = (int)(json_dict["year"])
        id_cnt = len(ids)

        score_stv_list = []
        abs_paper = json_dict["researcher_paper_abstract_in_json_file"]
        abs_list = json_dict["researcher_nsf_project_abstract"]
        abs_list.append(abs_paper)
        embed_paper = embed(abs_list)
        with tf.Session() as sess:
            sess.run(tf.initialize_all_variables())
            sess.run(tf.initialize_all_tables())
            embed_list = sess.run(embed_paper)
            #print(embed_list)

        for i in range(id_cnt):
            id = (int)(ids[i])
            lsi_score = (float)(score_lsi_list[i])
            lda_score = (float)(score_lda_list[i])
            stv_score = np.linalg.norm(embed_list[i] - embed_list[id_cnt])
            stv_score = 1.0 / (1.0 + stv_score)
            score_stv_list.append(stv_score)

            if year >= 2015 and year <= 2017:
                dict_authors[id]["lsi_score_after_2015"].append(lsi_score)
                dict_authors[id]["lda_score_after_2015"].append(lda_score)
                dict_authors[id]["stv_score_after_2015"].append(stv_score)
                dict_authors[id]["paper_numbers_after_2015"] += 1
                dict_authors[id]["max_lsi_score_after_2015"] = max(dict_authors[id]["max_lsi_score_after_2015"], lsi_score)
                dict_authors[id]["max_lda_score_after_2015"] = max(dict_authors[id]["max_lda_score_after_2015"], lda_score)
                dict_authors[id]["max_stv_score_after_2015"] = max(dict_authors[id]["max_stv_score_after_2015"], stv_score)
            else:
                dict_authors[id]["lsi_score_before_2015"].append(lsi_score)
                dict_authors[id]["lda_score_before_2015"].append(lda_score)
                dict_authors[id]["stv_score_before_2015"].append(stv_score)
                dict_authors[id]["paper_numbers_before_2015"] += 1
                dict_authors[id]["max_lsi_score_before_2015"] = max(dict_authors[id]["max_lsi_score_before_2015"], lsi_score)
                dict_authors[id]["max_lda_score_before_2015"] = max(dict_authors[id]["max_lda_score_before_2015"], lda_score)
                dict_authors[id]["max_stv_score_before_2015"] = max(dict_authors[id]["max_stv_score_before_2015"], stv_score)

            dict_authors[id]["max_lsi_score"] = max(dict_authors[id]["max_lsi_score"], lsi_score)
            dict_authors[id]["max_lda_score"] = max(dict_authors[id]["max_lda_score"], lda_score)
            dict_authors[id]["max_stv_score"] = max(dict_authors[id]["max_stv_score"], stv_score)
            dict_authors[id]["min_lsi_score"] = min(dict_authors[id]["min_lsi_score"], lsi_score)
            dict_authors[id]["min_lda_score"] = min(dict_authors[id]["min_lda_score"], lda_score)
            dict_authors[id]["min_stv_score"] = min(dict_authors[id]["min_stv_score"], stv_score)
            dict_authors[id]["paper_numbers_all"] += 1

        print(score_stv_list)
        json_dict["score_stv"] = score_stv_list
        
        with open('info_stv_papers_2015.json', 'a', encoding='utf-8') as fo:
            new_string = json.dumps(json_dict)
            fo.write(new_string)
            fo.write("\n")
        cnt += 1
        if cnt % 10 == 0:
            print("json summarize finished", cnt)


author_cnt = 0
with open('info_all_projects_2015.json', 'w', encoding='utf-8') as fo:
    for i in range(13905):
        new_dict = dict_authors[i]
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


        
