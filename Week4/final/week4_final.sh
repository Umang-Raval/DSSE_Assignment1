#!/bin/bash

#SBATCH --job-name=week4_final_v3
#SBATCH --output=logs/final_%j.log
#SBATCH --error=logs/final_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:2
#SBATCH --time=12:00:00
#SBATCH --mem=180G

echo "STARTING FINAL ARCHITECTURE RECOVERY"

module purge

module load lang/Python/3.10.4-GCCcore-11.3.0
module load system/CUDA/12.4.0

source /scratch/hpc-prf-dssecs/group5/llm/bin/activate

export HF_HOME=/scratch/hpc-prf-dssecs/group5/huggingface_cache
export TRANSFORMERS_CACHE=/scratch/hpc-prf-dssecs/group5/huggingface_cache
export HUGGINGFACE_HUB_CACHE=/scratch/hpc-prf-dssecs/group5/huggingface_cache

cd /scratch/hpc-prf-dssecs/group5/week4_v3/final

python week4_final_architecture.py

echo "FINAL ARCHITECTURE RECOVERY DONE"
