# similarity

## 运行顺序

### lsi/lda

#### 1. init.py 

初始化数据提供给clear.cpp去除文本中的乱码，修改数据格式 </br>
输入
```
    nsfinfor2015.json(格式见/input_example/info_100_nsfinfor.json) 
    exportAwards-2015.xls
```

输出：
```
    all_texts_151617.txt
```

#### 2. clear.cpp

去除乱码 </br>
输入:
```
    all_texts_151617.txt
```

输出：
```
    clear_texts_151617.txt
```

#### 3. work.py

主程序 </br>
输入：
```
    exportAwards-2015.xls
    nsfinfor2015.json
    clear_texts_151617.txt
```

输出：
```
    info_all_projects.json
```

### tensorflow

#### tf_google_2015.py

输入：
```
    info_all_papers_2015.json
    exportAwards-2015.xls
```

输出：
```
    info_all_projects_2015.json(/output_example)
```

## 样例

### 输入

/input_example

#### nsfinfor2015.json

```json
    {
        "citation": 0, 
        "abstract": "", 
        "year": 2012, 
        "authors": [
            "Jeremy B. Wright", 
            "George T. Wang", 
            "Weng Wah Chow", 
            "Qiming Li", 
            "Ting Shan Luk", 
            "Igal Brener", 
            "Luke F. Lester", 
            "Huiwen Xu"
        ], 
        "keywords": "", 
        "org": [
            "", 
            "", 
            "", 
            "", 
            "", 
            "", 
            "", 
            ""
        ], 
        "id": 6158, 
        "doi": "", 
        "title": "Lasing from Top-Down Gallium Nitride Nanowires.", 
        "feild": "", 
        "ori_name": "Luke F Lester"
    }
```

#### info_all_projects.json

```json
    {"researcher_id": [8531, 12650], "researcher_name_in_nsf_list": "Ming  Xu", "researcher_paper_title_in_json_file": "Maintaining Connectivity of MANETs through Multiple Unmanned Aerial Vehicles", "projects_cnt": 2, "year": 2015, "paper_citation": 0, "score_lda": ["0.000982033", "0.110548"], "field": ["Simulation", "Engineering", "Distributed computing", "Computer security"], "researcher_nsf_project_abstract": ["This project will advance the science and engineering of Food-Energy-Water (FEW) nexus modeling by developing and applying an integrated systems modeling framework. The modeling framework will enable quantitative characterization of urban FEW nexus, identify areas for efficiency improvement, and evaluate the consequences of policy and technology scenarios."], "researcher_paper_abstract_in_json_file": "Recently, Unmanned Aerial Vehicles (UAVs) have emerged as relay platforms to maintain the connectivity of ground mobile ad hoc networks (MANETs).", "paper_keywords": "", "score_lsi": ["0.119706", "0.0795219"]}
```

### 输出

/output_example

#### info_all_projects_2015.json

```json
    {"researcher_name": "Mark Warschauer", "lda_score_before_2015": [0.205141, 0.700193, 0.985884, 0.994071, 0.931025, 0.984773, 0.685481, 0.938277, 0.723713, 0.961439, 0.898945, 0.955096, 0.981834, 0.891237, 0.981719, 0.994733, 0.950794, 0.884582, 0.917516, 0.639449, 0.985477, 0.873115, 0.944505], "max_lda_score": 0.994733, "max_lda_score_after_2015": 0.964947, "paper_numbers_all": 32, "min_lsi_score": 0.0292507, "max_lsi_score_before_2015": 0.890608, "max_lda_score_before_2015": 0.994733, "lda_score_after_2015": [0.964947, 0.871679, 0.878375, 0.530081, 0.823967, 0.61633, 0.858441, 0.953091, 0.576256], "paper_numbers_before_2015": 23, "lsi_score_before_2015": [0.0779257, 0.60253, 0.79758, 0.865468, 0.622391, 0.887361, 0.0854057, 0.645695, 0.714859, 0.637595, 0.386117, 0.35799, 0.695614, 0.451247, 0.720509, 0.811888, 0.573102, 0.482408, 0.46055, 0.0292507, 0.890608, 0.457449, 0.434221], "min_lda_score": 0.205141, "lsi_score_after_2015": [0.831976, 0.685306, 0.657008, 0.702806, 0.686424, 0.768132, 0.648994, 0.645602, 0.723469], "researcher_id": 1, "paper_numbers_after_2015": 9, "max_lsi_score_after_2015": 0.831976, "max_lsi_score": 0.890608}
```
