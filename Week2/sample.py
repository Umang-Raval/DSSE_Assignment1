# ==========================================
# 0. IMPORT THE REQUIRED DEPENDENCIES
# ==========================================

import os
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)

# ==========================================
# 1. ENVIRONMENT & MODEL SETUP
# ==========================================

model_name = "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"

hf_token = os.environ.get('HF_TOKEN')

if not hf_token:
    print("WARNING: HF_TOKEN not found.")

# Clear GPU cache
torch.cuda.empty_cache()

# ==========================================
# Hardware optimization (Quantization)
# Required because Nemotron 70B is too large
# for 2x A100 GPUs in full precision
# ==========================================

print("Configuring 4-bit quantization...")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

# ==========================================
# 2. LOAD THE TOKENIZER
# ==========================================

print(f"Loading Tokenizer for {model_name}...")

tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    token=hf_token,
    trust_remote_code=True
)

tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "left"

# ==========================================
# 3. LOAD THE MODEL
# ==========================================

print("Loading Model across 2x A100 GPUs...")

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    token=hf_token,
    trust_remote_code=True,
    quantization_config=bnb_config,
    device_map="auto",
    dtype=torch.bfloat16
)

print("Model loaded successfully!")

# ==========================================
# 4. INFERENCE PIPELINE
# ==========================================

# Design the prompt
messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful software assistant. "
            "Your job is to explain the functionality "
            "of the provided code in simple terms."
        )
    },
    {
        "role": "user",
        "content": """Please analyze the following source code:

<source_code>

public class Task2 {

    public static void main(String[] args) {

        String id1 = "AMQ-2104";
        double files = 8.0;

        String id2 = "AMQ-317";
        double dmm = 0.45;

        int n = Integer.parseInt(id1.split("-")[1])
            + Integer.parseInt(id2.split("-")[1]);

        int digits = 0;

        while (n > 0) {
            n = n / 10;
            digits++;
        }

        int impact = (int) (files * dmm);

        System.out.println("Combined digits: " + digits);
        System.out.println("Impact: " + impact);
    }
}

</source_code>
"""
    }
]

# ==========================================
# TOKENIZATION
# ==========================================

print("Preparing prompt...")

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt"
)

# Move inputs safely to GPUs
inputs = {k: v.to(model.device) for k, v in inputs.items()}

# ==========================================
# MODEL INFERENCE
# ==========================================

print("Generating response...\n")

torch.cuda.empty_cache()

outputs = model.generate(
    **inputs,
    max_new_tokens=1024,
    temperature=0.5,
    top_p=0.8,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id
)

# ==========================================
# DECODE OUTPUT
# ==========================================

input_length = inputs['input_ids'].shape[1]

response = tokenizer.decode(
    outputs[0][input_length:],
    skip_special_tokens=True
)

# ==========================================
# DISPLAY OUTPUT
# ==========================================

print("\n--- Model Output ---\n")

print(response)

print("\n==========================================")