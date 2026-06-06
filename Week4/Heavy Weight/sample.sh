#!/bin/bash

# =========================================================
# SLURM CONFIGURATION
# =========================================================

#SBATCH --job-name="hsummarization_70b"
#SBATCH --time=08:00:00
#SBATCH --gres=gpu:a100:2
#SBATCH --cpus-per-task=16
#SBATCH --partition=gpu
#SBATCH --mem=240G
#SBATCH --output=hsummarization_%j.log

# =========================================================
# 1. LOAD MODULES
# =========================================================

module purge

module load lang/Python/3.10.4-GCCcore-11.3.0

module load system/CUDA/12.4.0

source /scratch/hpc-prf-dssecs/group5/llm/bin/activate

export HF_HOME=/scratch/hpc-prf-dssecs/group5/huggingface_cache

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

export HF_TOKEN="YOUR_HF_TOKEN"

echo "Starting Hierarchical Summarization 70B job...Week4..."

cd /scratch/hpc-prf-dssecs/group5/pawanw4

echo "Started: $(date)"
echo "Running hierarchical summarization..."

python -u sample.py

echo "Finished: $(date)"

