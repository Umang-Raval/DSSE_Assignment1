# 📊 DSSE Assignment 1 – Group 5  
## Hadoop YARN ResourceManager – Architectural Analysis

---

## 📌 Project Overview
This project analyzes the architecture of the Hadoop YARN ResourceManager, focusing on the scheduler and capacity components. The goal is to extract dependencies from the system and apply clustering algorithms to understand architectural structure.

---

## 🎯 Research Questions
1. How do different clustering algorithms vary in identifying architectural components?
2. How effectively can dependency extraction support architectural understanding?

---

## 👥 Team Members
- Keshav Indrabhushan Purohit  
- Rahul Vinod Borana  
- Umang Arvindbhai Raval  
- Pawankumar Ravish  
- Sangsaptak Pal  

---

## ⚖️ Work Distribution (Equal Contribution)
All team members equally contributed to:
- Environment setup  
- Hadoop build  
- Dependency extraction  
- Filtering  
- Clustering (WCA, LIMBO, ACDC)  
- Result validation  
- Documentation  

---

# ⚙️ Step-by-Step Execution Guide

## 🔹 Step 1: Clone Hadoop Repository
    git clone https://github.com/apache/hadoop.git
    cd hadoop

---

## 🔹 Step 2: Build Hadoop (Generate JAR)
    mvn clean package -DskipTests

✔ Output:
    hadoop-yarn-server-resourcemanager-3.6.0-SNAPSHOT.jar

---

## 🔹 Step 3: Extract Full Dependencies (ARCADE JavaParser)
    java -jar arcade_tools/arcade_core_JavaParser.jar \
    /home/umang/Desktop/DSSE/hadoop/hadoop/hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-resourcemanager/target/hadoop-yarn-server-resourcemanager-3.6.0-SNAPSHOT.jar \
    output/YARN_full.rsf \
    output/YARN_full.fv \
    "org.apache.hadoop.yarn"

✔ Output Logs:
- 1181 classes analysed  
- 353 strong components  
- 68 packages  
- 17 package components  

✔ Count total dependencies:
    wc -l output/YARN_full.rsf

✔ Result:
    10036 output/YARN_full.rsf

---

## 🔹 Step 4: Filter Relevant Dependencies (Scheduler Capacity)
    grep "scheduler.capacity" output/YARN_full.rsf > output/yarn_filtered.rsf

✔ Count filtered dependencies:
    wc -l output/yarn_filtered.rsf

✔ Result:
    3935 output/yarn_filtered.rsf

---

## 🔹 Step 5: Run Clustering Algorithms

### ▶️ WCA
    java -Xmx4g -jar arcade_tools/arcade_core_clusterer.jar \
    algo=WCA language=java \
    deps=output/yarn_filtered.rsf measure=UEM \
    projname=WCA projpath=WCA projversion=1

---

### ▶️ LIMBO
    java -Xmx4g -jar arcade_tools/arcade_core_clusterer.jar \
    algo=LIMBO language=java \
    deps=output/yarn_filtered.rsf measure=IL \
    projname=LIMBO projpath=LIMBO projversion=1

---

### ▶️ ACDC
    java -jar arcade_tools/arcade_core-ACDC.jar \
    output/yarn_filtered.rsf ACDC/

---

## 🔹 Step 6: Evaluate Results

### ▶️ WCA
    echo "WCA Results:"
    wc -l WCA/*.rsf
    cut -d ' ' -f2 WCA/*.rsf | sort | uniq | wc -l

---

### ▶️ LIMBO
    echo "LIMBO Results:"
    wc -l LIMBO/*.rsf
    cut -d ' ' -f2 LIMBO/*.rsf | sort | uniq | wc -l

---

### ▶️ ACDC
    echo "ACDC Results:"
    wc -l ACDC/*.rsf
    cut -d ' ' -f2 ACDC/*.rsf | sort | uniq | wc -l

---

## 📈 Results Summary

| Algorithm | Lines | Clusters |
|----------|------|----------|
| WCA      | 744  | 50       |
| LIMBO    | 744  | 50       |
| ACDC     | 744  | 23       |

---

## 🔍 Observations

- Full system extraction → **10036 dependencies**
- Filtered (scheduler.capacity) → **3935 dependencies**
- WCA & LIMBO → **50 clusters** (fixed stopping criterion)
- ACDC → **23 clusters** (structure-based)
- All outputs → **744 relations**

✔ Key Insight:
- WCA/LIMBO → fine-grained clustering  
- ACDC → high-level architecture  

---

## 📚 Key Learnings
- Hadoop YARN ResourceManager internals  
- Large-scale dependency extraction  
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
    │   ├── YARN_full.rsf
    │   ├── YARN_full.fv
    │   └── yarn_filtered.rsf
    ├── hadoop/
    ├── arcade_tools/
    ├── filter.py

---

## 📌 Conclusion
WCA and LIMBO generate detailed fine-grained clusters, while ACDC produces meaningful higher-level architectural groupings. Filtering significantly improves analysis quality and relevance.

---

## 🔗 Repository
https://github.com/Umang-Raval/DSSE_Assignment1
