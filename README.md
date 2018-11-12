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
    {"researcher_id": [8531, 12650], "researcher_name_in_nsf_list": "Ming  Xu", "researcher_paper_title_in_json_file": "Maintaining Connectivity of MANETs through Multiple Unmanned Aerial Vehicles", "projects_cnt": 2, "year": 2015, "paper_citation": 0, "score_lda": ["0.000982033", "0.110548"], "field": ["Simulation", "Engineering", "Distributed computing", "Computer security"], "researcher_nsf_project_abstract": ["1605202 (Xu)\n\nThis project will advance the science and engineering of Food-Energy-Water (FEW) nexus modeling by developing and applying an integrated systems modeling framework. The modeling framework will enable quantitative characterization of urban FEW nexus, identify areas for efficiency improvement, and evaluate the consequences of policy and technology scenarios. Results from the case studies in Detroit and Beijing will guide policy and technology development for better managing FEW resources for these two testbeds as well as other similar cities in the U.S., in China, and around the world. The collaboration between the U.S. and China on this project provides opportunities for a group of researchers with diverse background to share data, expertise, and experience on modeling urban FEW nexus. The project will also engage stakeholders for seeking inputs to improve the modeling framework and scenarios. Research results will also be provided to stakeholders to support their decision making relevant to FEW nexus. Through the U.S.-China collaboration, unique opportunities will be created for a diverse group of graduate and undergraduate STEM students to conduct cutting-edge research in an international, interdisciplinary environment.\n\nThe research employs the latest knowledge from multiple disciplines for developing an integrated systems modeling framework to understand urban FEW nexus. Dynamic material flow analysis will characterize urban FEW resource stocks and flows. The structure and importance of network components will be examined using network-based metrics and methods from different but related fields (ecological network analysis and complex network analysis). Policy and technology scenarios will be evaluated using these network-based metrics and methods to identify co-benefits and avoid unintended consequences. The resulting urban FEW nexus modeling framework will address multiple dimensions and scales: systems (integrated FEW systems), spatial (key system processes that are both within and outside the city boundary), and temporal (short-term flows and long-term stocks). The modeling framework will also be applied to two distinct testbeds (Detroit and Beijing) for demonstration. While the case study results are specific for the testbeds, the integrated systems modeling framework will be generally applicable for understand the FEW nexus for other urban areas.", "1554349 (Xu)\n\nThis research aims to advance the current practice of developing Life Cycle Inventory (LCI) databases into a faster, less expensive process that still generates reliable LCI data. The research will (1) create a framework for modeling and analyzing LCI networks, (2) develop computational models for estimating missing LCI data, and (3) apply these models to evaluate LCI data quality and predict LCI data for emerging technologies. The education plan will (1) engage a diverse group of LCA practitioners during the course of the project, (2) deliver open source software add-ons for LCA practitioners to easily use the computational models developed in the proposed research, (3) develop an education theory grounded curriculum module incorporating research outcomes for broader dissemination, and (4) train undergraduate and graduate students with diverse background in STEM fields by engaging them in the research program and other education activities. \n\nThis research will develop computational approaches for estimating missing data in Life Cycle Inventory (LCI) databases based solely on limited known data, without relying on time-consuming, expensive empirical data collection. The approach transfers the latest knowledge from network science to LCI database development. An LCI database represents the interdependence of unit processes and environmental interventions. The ensemble of such interdependence characterizes the structure of the underlying technology network (or LCI network). If sufficient enough, observed LCI data, although limited, can be used to extract structural features of the underlying LCI network. Such structural features, in turn, can be used to predict the structure of the unknown area of the LCI network, which is equivalent to estimating the unknown data in the LCI database. This research will first create a framework for modeling and analyzing LCI networks. This framework will then be used to develop and validate a variety of link prediction models to estimate missing data for LCI databases. Finally the validated link prediction models will be used to evaluate LCI data quality and predict LCI data for emerging technologies for testbed databases selected in consultation with stakeholders."], "researcher_paper_abstract_in_json_file": "Recently, Unmanned Aerial Vehicles (UAVs) have emerged as relay platforms to maintain the connectivity of ground mobile ad hoc networks (MANETs). However, when deploying UAVs, existing methods have not consider one situation that there are already some UAVs deployed in the field. In this paper, we study a problem jointing the motion control of existing UAVs and the deployment of new UAVs so that the number of new deployed UAVs to maintain the connectivity of ground MANETs can be minimized. We firstly formulate the problem as a Minimum Steiner Tree problem with Existing Mobile Steiner points under Edge Length Bound constraints (MST-EMSELB) and prove the NP completeness of this problem. Then we propose three Existing UAVs Aware (EUA) approximate algorithms for the MST-EMSELB problem: Deploy-Before-Movement (DBM), Move-Before-Deployment (MBD), and Deploy-Across-Movement (DAM) algorithms. Both DBM and MBD algorithm decouple the joint problem and solve the deployment and movement problem one after another, while DAM algorithm optimizes the deployment and motion control problem crosswise and solves these two problems simultaneously. Simulation results demonstrate that all EUA algorithms have better performance than non-EUA algorithm. The DAM algorithm has better performance in all scenarios than MBD and DBM ones. Compared with DBM algorithm, the DAM algorithm can reduce at most 70&#x25; of the new UAVs number.", "paper_keywords": "", "score_lsi": ["0.119706", "0.0795219"]}
```

### 输出

/output_example

#### info_all_projects_2015.json

```json
    {"researcher_name": "Mark Warschauer", "lda_score_before_2015": [0.205141, 0.700193, 0.985884, 0.994071, 0.931025, 0.984773, 0.685481, 0.938277, 0.723713, 0.961439, 0.898945, 0.955096, 0.981834, 0.891237, 0.981719, 0.994733, 0.950794, 0.884582, 0.917516, 0.639449, 0.985477, 0.873115, 0.944505], "max_lda_score": 0.994733, "max_lda_score_after_2015": 0.964947, "paper_numbers_all": 32, "min_lsi_score": 0.0292507, "max_lsi_score_before_2015": 0.890608, "max_lda_score_before_2015": 0.994733, "lda_score_after_2015": [0.964947, 0.871679, 0.878375, 0.530081, 0.823967, 0.61633, 0.858441, 0.953091, 0.576256], "paper_numbers_before_2015": 23, "lsi_score_before_2015": [0.0779257, 0.60253, 0.79758, 0.865468, 0.622391, 0.887361, 0.0854057, 0.645695, 0.714859, 0.637595, 0.386117, 0.35799, 0.695614, 0.451247, 0.720509, 0.811888, 0.573102, 0.482408, 0.46055, 0.0292507, 0.890608, 0.457449, 0.434221], "min_lda_score": 0.205141, "lsi_score_after_2015": [0.831976, 0.685306, 0.657008, 0.702806, 0.686424, 0.768132, 0.648994, 0.645602, 0.723469], "researcher_id": 1, "paper_numbers_after_2015": 9, "max_lsi_score_after_2015": 0.831976, "max_lsi_score": 0.890608}
```