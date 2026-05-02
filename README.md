# 📊 DSSE Assignment 1 – Group 5  
## Hadoop YARN ResourceManager – Architectural Analysis

---

## 📌 Project Overview
This project focuses on analyzing the architecture of the Hadoop YARN ResourceManager, specifically its scheduler and capacity components.

The objective of this assignment is to extract class-level dependencies from a large-scale Java system and apply clustering algorithms to recover its architectural structure.

---

## 🎯 Research Questions
1. How do different clustering algorithms vary in their ability to determine architectural components?
2. How effectively can dependency extraction support architectural understanding?

---

## 👥 Team Members
- Keshav Indrabhushan Purohit  
- Rahul Borana  
- Umang Raval  
- Pawan  
- Sangsa Pal  

---

## ⚖️ Work Distribution (Equal Contribution)
All team members contributed equally across all stages:
- Environment setup and Hadoop build  
- Dependency extraction using ARCADE JavaParser  
- Filtering relevant ResourceManager components  
- Running clustering algorithms (WCA, LIMBO, ACDC)  
- Result validation and analysis  
- Documentation and reporting  

---

## ⚙️ Technical Workflow

### 1. Build Hadoop Project
    mvn clean package -DskipTests

Generated:
    hadoop-yarn-server-resourcemanager-3.6.0-SNAPSHOT.jar

---

### 2. Full Dependency Extraction
    java -jar arcade_tools/arcade_core_JavaParser.jar \
    /home/umang/Desktop/DSSE/hadoop/hadoop/hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-resourcemanager/target/hadoop-yarn-server-resourcemanager-3.6.0-SNAPSHOT.jar \
    output/YARN_full.rsf \
    output/YARN_full.fv \
    "org.apache.hadoop.yarn"

Output:
- 1181 classes analyzed  
- 353 strong components  
- 68 packages  
- 17 package-level components  

Line count:
    wc -l output/YARN_full.rsf

Result:
    10036 output/YARN_full.rsf

---

### 3. Filter Dependencies
    grep "scheduler.capacity" output/YARN_full.rsf > output/yarn_filtered.rsf

Line count:
    wc -l output/yarn_filtered.rsf

Result:
    3935 output/yarn_filtered.rsf

---

### 4. Clustering Algorithms

WCA:
    java -Xmx4g -jar arcade_tools/arcade_core_clusterer.jar \
    algo=WCA language=java \
    deps=output/yarn_filtered.rsf measure=UEM \
    projname=WCA projpath=WCA projversion=1

LIMBO:
    java -Xmx4g -jar arcade_tools/arcade_core_clusterer.jar \
    algo=LIMBO language=java \
    deps=output/yarn_filtered.rsf measure=IL \
    projname=LIMBO projpath=LIMBO projversion=1

ACDC:
    java -jar arcade_tools/arcade_core-ACDC.jar \
    output/yarn_filtered.rsf ACDC/

---

## 📈 Results

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
- Full extraction: 10036 dependencies  
- Filtered dependencies: 3935  
- WCA & LIMBO: 50 clusters (fixed threshold)  
- ACDC: 23 clusters (structure-based)  
- All clustering outputs: 744 relations  

Insight:
- WCA/LIMBO → fine-grained clustering  
- ACDC → higher-level architecture  

---

## 📚 Key Learnings
- Hadoop YARN architecture understanding  
- Large-scale Java dependency analysis  
- ARCADE tool usage  
- Clustering-based architecture recovery  
- Importance of filtering  

---

## 📂 Project Structure
    DSSE_Assignment1/
    ├── ACDC/
    ├── LIMBO/
    ├── WCA/
    ├── output/
    ├── hadoop/
    ├── arcade_tools/
    ├── tools/
    ├── filter.py

---

## 🚀 How to Run
1. Build:
    mvn clean package -DskipTests

2. Extract:
    java -jar arcade_core_JavaParser.jar ...

3. Filter:
    grep "scheduler.capacity" ...

4. Cluster:
    WCA / LIMBO / ACDC

5. Evaluate:
    wc -l + cut commands

---

## 📌 Conclusion
WCA and LIMBO produce fine-grained clusters, while ACDC captures higher-level architecture. Filtering significantly improves the quality of analysis.

---

## 🔗 Repository
https://github.com/Umang-Raval/DSSE_Assignment1
