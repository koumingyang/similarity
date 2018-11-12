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
### 输出
/output_example