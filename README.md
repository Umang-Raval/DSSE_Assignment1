# DSSE Assignment 1 – Group 5

## Overview

This repository contains the complete implementation and analysis for Assignment 1 of the Data Science for Software Engineering (DSSE) course.

The project investigates software architecture recovery for the Hadoop YARN Capacity Scheduler using a combination of:

- Structural clustering
- Semantic clustering
- Large Language Models (LLMs)
- Hierarchical architectural summarization

The work was completed over four weeks and culminates in an automated architectural recovery pipeline capable of generating high-level architectural descriptions from source code.

---

## Team Members

| Name                        | Contribution                                                    |
| --------------------------- | --------------------------------------------------------------- |
| Umang Arvindbhai Raval      | Heavyweight HPC deployment, prompt engineering, model execution |
| Pawankumar Ravish           | Heavyweight pipeline development and automation                 |
| Keshav Indrabhushan Purohit | Lightweight model implementation                                |
| Rahul Vinod Borana          | Lightweight pipeline validation and evaluation                  |
| Sangsaptak Pal              | Documentation, report preparation and QA                        |

---

# Week 1 – Dependency Extraction and Structural Clustering

## Objective

Extract structural dependencies from Hadoop YARN and generate architectural clusters.

## Activities

- Compiled Hadoop project
- Generated dependency RSF files
- Filtered Capacity Scheduler components
- Generated clusters using:
  - WCA
  - ACDC
  - LIMBO

## Deliverables

- Filtered dependency RSF
- ACDC cluster RSF
- LIMBO cluster RSF
- WCA cluster RSF

---

# Week 2 – Cluster Evaluation and LLM Preparation

## Objective

Evaluate clustering quality and prepare LLM environments.

## Activities

- Calculated architecture similarity metrics
- Compared clustering outputs
- Configured lightweight and heavyweight LLM environments
- Tested prompting strategies

## Models Assigned

### Lightweight

- ByteDance/Seed-Coder-8B-Instruct

### Heavyweight

- NVIDIA/Llama-3.1-Nemotron-70B-Instruct-HF

---

# Week 3 – Semantic Clustering

## Objective

Generate semantic clusters by combining structural and semantic information.

## Activities

- Generated code embeddings
- Calculated cosine similarity matrices
- Combined semantic and structural similarity
- Applied ARC clustering

## Deliverables

- ARC cluster RSF
- Evaluation metrics
- Similarity matrices

---

# Week 4 – LLM-Based Architectural Recovery

## Objective

Recover architectural descriptions using hierarchical summarization.

## Three-Level Hierarchical Pipeline

### Level 1 – File Summarization

Each Java file is summarized independently.

Outputs:

- Purpose
- Key functionality
- Core logic
- Inputs/Outputs
- Dependencies

### Level 2 – Subdirectory Summarization

File summaries are aggregated into package-level summaries.

### Level 3 – Cluster Summarization

Subdirectory summaries are combined to generate:

- Architectural title
- Architectural description
- Component responsibilities
- Interactions

---

## Lightweight Implementation

Environment:

- Google Colab
- NVIDIA T4 GPU
- ByteDance Seed-Coder-8B-Instruct
- 4-bit Quantization

Outputs:

- File summaries
- Subdirectory summaries
- Cluster summaries

---

## Heavyweight Implementation

Environment:

- University HPC Cluster
- Dual NVIDIA A100 GPUs
- NVIDIA Llama-3.1-Nemotron-70B-Instruct-HF
- SLURM

Outputs:

- File summaries
- Subdirectory summaries
- Cluster summaries
- CSV architectural recovery reports

---

# Research Questions

1. How do different clustering algorithms vary in their ability to determine architectural components?

2. How do different prompting techniques impact an LLM's ability to describe architectural components from source code?

3. Can lightweight models achieve architectural recovery quality comparable to heavyweight models?

---

# Key Findings

- ARC produced the most semantically coherent clusters.
- Hierarchical summarization reduced context-window limitations.
- Structured prompts improved architectural descriptions.
- Lightweight models successfully recovered architecture on commodity hardware.
- Heavyweight models generated richer and more consistent summaries.

---

# Technologies Used

- Python
- Hadoop YARN
- ARCADE
- Google Colab
- SLURM
- PyTorch
- Hugging Face Transformers
- BitsAndBytes

---

# References

- Hadoop YARN
- ARCADE Framework
- ByteDance Seed-Coder-8B-Instruct
- NVIDIA Llama-3.1-Nemotron-70B-Instruct-HF
