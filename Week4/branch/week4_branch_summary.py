import os
import sys
import time
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)

# ==========================================
# IMPORT UTILS
# ==========================================

sys.path.append("../utils")

from hierarchy_utils import group_by_package

# ==========================================
# MODEL CONFIG
# ==========================================

MODEL_NAME = "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"

HF_TOKEN = os.environ.get("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found")

# ==========================================
# QUANTIZATION
# ==========================================

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

# ==========================================
# LOAD TOKENIZER
# ==========================================

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    token=HF_TOKEN,
    trust_remote_code=True
)

tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "left"

# ==========================================
# LOAD MODEL
# ==========================================

print("Loading model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    token=HF_TOKEN,
    trust_remote_code=True,
    quantization_config=bnb_config,
    device_map="auto",
    dtype=torch.bfloat16
)

print("Model loaded!")

# ==========================================
# SUMMARY DIRECTORY
# ==========================================

summary_dir = "../leaf/summaries"

groups = group_by_package(summary_dir)

print(f"\nDetected {len(groups)} packages")

# ==========================================
# PROCESS EACH PACKAGE
# ==========================================

for package, files in groups.items():

    try:

        print("\n====================================")
        print(f"PACKAGE: {package}")
        print(f"FILES: {len(files)}")
        print("====================================")

        combined = ""

        # ==========================================
        # LOAD FILE SUMMARIES
        # ==========================================

        for file in files:

            with open(file, "r", encoding="utf-8") as f:

                combined += f.read()
                combined += "\n\n"

        # ==========================================
        # PROMPT
        # ==========================================

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior distributed systems "
                    "architect specializing in Hadoop YARN."
                )
            },
            {
                "role": "user",
                "content": f"""
The following semantic summaries belong to one
Hadoop YARN Capacity Scheduler package.

Perform architectural recovery.

Generate ALL sections completely:

1. Module Title
2. Architectural Purpose
3. Main Responsibilities
4. Component Interactions
5. Scheduling Behavior
6. Resource Allocation Behavior
7. Queue Management Logic
8. Preemption Logic (if applicable)
9. Important Dependencies
10. Design Patterns
11. Distributed Systems Observations

IMPORTANT:
- Focus on architecture recovery
- Explain subsystem behavior
- Explain interactions between components
- Do NOT summarize files individually
- Generate COMPLETE output
- Do not stop mid-sentence

SUMMARIES:

{combined}
"""
            }
        ]

        # ==========================================
        # TOKENIZE
        # ==========================================

        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        )

        inputs = {
            k: v.to(model.device)
            for k, v in inputs.items()
        }

        print("Generating summary...")

        start_time = time.time()

        # ==========================================
        # GENERATE
        # ==========================================

        outputs = model.generate(
            **inputs,
            max_new_tokens=1200,
            min_new_tokens=500,
            temperature=0.2,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id
        )

        end_time = time.time()

        print(f"Completed in {end_time - start_time:.2f} sec")

        # ==========================================
        # DECODE
        # ==========================================

        input_len = inputs["input_ids"].shape[1]

        response = tokenizer.decode(
            outputs[0][input_len:],
            skip_special_tokens=True
        )

        # ==========================================
        # SAVE
        # ==========================================

        output_file = (
            f"package_summaries/{package}_summary.txt"
        )

        with open(output_file, "w", encoding="utf-8") as out:
            out.write(response)

        print(f"Saved: {output_file}")

    except Exception as e:

        print(f"ERROR: {str(e)}")

        with open("logs/errors.txt", "a") as err:

            err.write(f"\nPACKAGE: {package}\n")
            err.write(str(e))
            err.write("\n=============================\n")

print("\nALL PACKAGE SUMMARIES COMPLETED")