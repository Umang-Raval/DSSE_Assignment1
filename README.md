# 📊 DSSE Assignment 1 – Group 5  
## Hadoop YARN ResourceManager – Architectural Analysis

---

## 📌 Project Overview
This project focuses on analyzing the architecture of the Hadoop YARN ResourceManager, specifically its scheduler and capacity components.

The objective is to extract class dependencies and evaluate clustering algorithms to understand how software architecture can be recovered automatically.

---

## 🎯 Research Questions
1. How do different clustering algorithms vary in their ability to determine architectural components?
2. How can extracted dependencies help in understanding system structure?

---

## 👥 Team Members
- Keshav Indrabhushan Purohit  
- Rahul Borana  
- Umang Raval  
- Pawan  
- Sangsaptak Pal 

---

## ⚖️ Work Distribution (Equal Contribution)

Each team member contributed equally across all stages:

- Environment setup and Hadoop build  
- Dependency extraction using ARCADE  
- Filtering relevant ResourceManager components  
- Running clustering algorithms (WCA, LIMBO, ACDC)  
- Result validation and analysis  
- Documentation and reporting  

---

## ⚙️ Technical Workflow

### 1. Build Hadoop Project
    mvn clean package -DskipTests

Generates:
    hadoop-yarn-server-resourcemanager-3.6.0-SNAPSHOT.jar

---

### 2. Dependency Extraction (ARCADE JavaParser)
    java -jar arcade_core_JavaParser.jar \
    hadoop-yarn-server-resourcemanager-3.6.0-SNAPSHOT.jar \
    Output/output.rsf Output/outputfv.fv \
    "org.apache.hadoop.yarn.server.resourcemanager"

Outputs:
- output.rsf → dependency relations  
- outputfv.fv → feature vectors  

---

### 3. Dependency Filtering
    grep "scheduler.capacity" Output/output.rsf > Output/filtered.rsf

---

### 4. Clustering Algorithms

WCA:
    java -Xmx4g -jar arcade_core_clusterer.jar \
    algo=WCA language=java \
    deps=Output/filtered.rsf measure=UEM \
    projname=WCA projpath=WCA projversion=1

LIMBO:
    java -Xmx4g -jar arcade_core_clusterer.jar \
    algo=LIMBO language=java \
    deps=Output/filtered.rsf measure=IL \
    projname=LIMBO projpath=LIMBO projversion=1

ACDC:
    java -jar arcade_core-ACDC.jar \
    Output/filtered.rsf ACDC/

---

## 📈 Results

Commands Used:

    echo "WCA Results:"
    wc -l WCA/*.rsf
    cut -d ' ' -f2 WCA/*.rsf | sort | uniq | wc -l

    echo "LIMBO Results:"
    wc -l LIMBO/*.rsf
    cut -d ' ' -f2 LIMBO/*.rsf | sort | uniq | wc -l

    echo "ACDC Results:"
    wc -l ACDC/*.rsf
    cut -d ' ' -f2 ACDC/*.rsf | sort | uniq | wc -l

---

### Output Summary

| Algorithm | Lines | Clusters |
|----------|------|----------|
| WCA      | 744  | 50       |
| LIMBO    | 744  | 50       |
| ACDC     | 744  | 23       |

---

## 🔍 Observations

- WCA and LIMBO produced 50 clusters due to predefined stopping criteria
- These algorithms generate fine-grained clusters
- ACDC produced 23 clusters based on structural patterns
- ACDC captures higher-level architectural components

This highlights the difference between fixed clustering approaches and structure-based clustering.

---

## 📚 Key Learnings

- Understanding of Hadoop YARN architecture  
- Experience with large-scale Java systems  
- Practical use of ARCADE toolchain  
- Insights into software clustering techniques  
- Dependency-based architectural recovery  

---

## 📂 Project Structure

    DSSE_Assignment1/
    │
    ├── ACDC/
    ├── LIMBO/
    ├── WCA/
    ├── output/
    ├── hadoop/
    ├── arcade_tools/
    ├── filter.py
    └── cut

---

## 🚀 How to Run

1. Build Hadoop:
    mvn clean package -DskipTests

2. Extract dependencies:
    java -jar arcade_core_JavaParser.jar ...

3. Filter dependencies:
    grep "scheduler.capacity" ...

4. Run clustering:
    WCA / LIMBO / ACDC commands

5. Evaluate:
    wc -l + cut commands

---

## 📌 Conclusion

This assignment demonstrates how clustering algorithms can be used to recover software architecture from source code.

- WCA and LIMBO produce fine-grained clusters  
- ACDC produces higher-level architectural components  

These results provide a strong foundation for further analysis in upcoming phases.

---

## 🔗 Repository
https://github.com/Umang-Raval/DSSE_Assignment1
