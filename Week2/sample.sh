#!/bin/bash

# =========================================================
# SLURM CONFIGURATION
# =========================================================

#SBATCH --job-name="nemotron70b"
#SBATCH --time=04:00:00
#SBATCH --gres=gpu:a100:2
#SBATCH --partition=gpu
#SBATCH --mem=240G
#SBATCH --output=nemotron_%j.log

# =========================================================
# 1. LOAD MODULES
# =========================================================

module purge

module load lang/Python/3.10.4-GCCcore-11.3.0
module load system/CUDA/12.4.0

# =========================================================
# 2. ACTIVATE VIRTUAL ENVIRONMENT
# =========================================================

source /scratch/hpc-prf-dssecs/group5/llm/bin/activate

# =========================================================
# 3. HUGGING FACE CACHE
# =========================================================

export HF_HOME=/scratch/hpc-prf-dssecs/group5/huggingface_cache

# =========================================================
# 4. PYTORCH MEMORY OPTIMIZATION
# =========================================================

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# =========================================================
# 5. HF TOKEN
# =========================================================

export HF_TOKEN=""
# =========================================================
# 6. EXECUTION
# =========================================================

echo "Starting Nemotron 70B job..."

python sample.py

echo "Job completed!"
