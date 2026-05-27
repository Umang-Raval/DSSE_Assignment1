import os
import time
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)

MODEL_NAME = "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"

HF_TOKEN = os.environ.get("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN missing")

torch.cuda.empty_cache()

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
# TOKENIZER
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
# MODEL
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
# LOAD FILE LIST
# ==========================================

with open("../input/capacity_files.txt", "r") as f:
    java_files = [x.strip() for x in f.readlines()]

print(f"Found {len(java_files)} Java files")

# ==========================================
# PROCESS FILES
# ==========================================

for java_file in java_files:

    try:

        print("\n====================================")
        print(f"PROCESSING: {java_file}")
        print("====================================")

        with open(java_file, "r", encoding="utf-8") as f:
            source_code = f.read()

        relative_path = java_file.split("capacity/")[-1]

        safe_name = relative_path.replace("/", "_")

        output_file = f"summaries/{safe_name}_summary.txt"

        if os.path.exists(output_file):
            print("Summary already exists")
            continue

        # ==========================================
        # CHUNK LARGE FILES
        # ==========================================

        chunks = [
            source_code[i:i+12000]
            for i in range(0, len(source_code), 12000)
        ]

        print(f"Total chunks: {len(chunks)}")

        chunk_summaries = []

        for idx, chunk in enumerate(chunks):

            print(f"Chunk {idx+1}/{len(chunks)}")

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a senior software architect "
                        "specializing in distributed Java systems "
                        "and Hadoop YARN."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
Analyze this Java source code chunk.

Extract:

1. Architectural role
2. Key functionality
3. Core logic
4. Inputs and outputs
5. Dependencies
6. Interactions with scheduler components

Keep the summary concise and technical.

SOURCE CODE:

{chunk}
"""
                }
            ]

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

            start_time = time.time()

            outputs = model.generate(
                **inputs,
                max_new_tokens=768,
                temperature=0.2,
                top_p=0.9,
                repetition_penalty=1.1,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )

            end_time = time.time()

            print(f"Chunk completed in {end_time - start_time:.2f} sec")

            input_len = inputs["input_ids"].shape[1]

            response = tokenizer.decode(
                outputs[0][input_len:],
                skip_special_tokens=True
            )

            chunk_summaries.append(response)

        # ==========================================
        # MERGE CHUNK SUMMARIES
        # ==========================================

        combined = "\n\n".join(chunk_summaries)

        merge_messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior software architect."
                )
            },
            {
                "role": "user",
                "content": f"""
Merge the following chunk summaries into ONE
coherent semantic file-level summary.

CHUNK SUMMARIES:

{combined}
"""
            }
        ]

        merge_inputs = tokenizer.apply_chat_template(
            merge_messages,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        )

        merge_inputs = {
            k: v.to(model.device)
            for k, v in merge_inputs.items()
        }

        outputs = model.generate(
            **merge_inputs,
            max_new_tokens=512,
            temperature=0.2,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        input_len = merge_inputs["input_ids"].shape[1]

        final_summary = tokenizer.decode(
            outputs[0][input_len:],
            skip_special_tokens=True
        )

        with open(output_file, "w", encoding="utf-8") as out:
            out.write(final_summary)

        print(f"Saved: {output_file}")

    except Exception as e:

        print(str(e))

        with open("logs/errors.txt", "a") as err:

            err.write(f"\nFILE: {java_file}\n")
            err.write(str(e))
            err.write("\n=============================\n")

print("\nALL FILES COMPLETED")
