import os
import time
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)

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
# LOAD PACKAGE SUMMARIES
# ==========================================

summary_dir = "../branch/package_summaries"

combined = ""

print("\nLoading package summaries...\n")

for file in os.listdir(summary_dir):

    path = os.path.join(summary_dir, file)

    print(f"Reading: {file}")

    with open(path, "r", encoding="utf-8") as f:

        combined += f.read()
        combined += "\n\n"

# ==========================================
# PROMPT
# ==========================================

messages = [
    {
        "role": "system",
        "content": (
            "You are an expert software architect "
            "specializing in distributed systems, "
            "resource schedulers, and Hadoop YARN."
        )
    },
    {
        "role": "user",
        "content": f"""
You are performing LLM-based architectural recovery
for the Hadoop YARN Capacity Scheduler subsystem.

The following package summaries were generated from:

- scheduler/capacity/
- scheduler/capacity/preemption/
- scheduler/capacity/allocator/
- scheduler/capacity/conf/
- scheduler/capacity/policy/
- scheduler/capacity/placement/
- scheduler/capacity/queuemanagement/

Recover the ACTUAL software architecture.

IMPORTANT:
- Use ONLY evidence from the summaries
- Avoid generic enterprise architecture terminology
- Do NOT invent UI layers or database layers
- Focus on distributed scheduling architecture
- Focus on queue management and resource allocation
- Explain subsystem responsibilities precisely
- Explain how components interact internally

Generate ALL sections completely:

1. Architecture Title

2. Core Architectural Layers
   - Capacity Scheduler Core
   - Queue Management
   - Resource Allocation
   - Preemption
   - Placement and Policies
   - Configuration Management

3. Queue Hierarchy Design
   - Root queues
   - Parent queues
   - Leaf queues
   - Dynamic queue behavior

4. Scheduling and Allocation Flow
   - Application submission
   - Queue placement
   - Resource assignment
   - Container allocation
   - Scheduling decisions

5. Resource Management Behavior
   - Capacity enforcement
   - User limits
   - Queue capacities
   - Resource tracking
   - Dynamic updates

6. Preemption and Enforcement Mechanisms
   - Queue balancing
   - Resource reclaiming
   - Killable containers
   - Scheduling fairness

7. Package/Submodule Responsibilities
   - allocator
   - preemption
   - placement
   - policy
   - conf
   - queuemanagement
   - capacity_core

8. Important Design Patterns
   - Strategy pattern
   - Template method
   - Hierarchical queue composition
   - Policy-driven scheduling

9. Distributed Systems Characteristics
   - Scalability
   - Fault tolerance
   - Cluster-wide coordination
   - Resource isolation

10. Final Architectural Assessment
   - Strengths
   - Limitations
   - Scheduler extensibility
   - Architectural observations

PACKAGE SUMMARIES:

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

print("\nGenerating final architecture report...\n")

start_time = time.time()

# ==========================================
# GENERATE
# ==========================================

outputs = model.generate(
    **inputs,
    max_new_tokens=1800,
    min_new_tokens=900,
    temperature=0.15,
    top_p=0.9,
    repetition_penalty=1.15,
    do_sample=True,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id
)

end_time = time.time()

print(f"Generation completed in {end_time - start_time:.2f} sec")

# ==========================================
# DECODE
# ==========================================

input_len = inputs["input_ids"].shape[1]

response = tokenizer.decode(
    outputs[0][input_len:],
    skip_special_tokens=True
)

# ==========================================
# SAVE REPORT
# ==========================================

output_dir = "architecture_reports"

os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(
    output_dir,
    "final_architecture.txt"
)

with open(output_file, "w", encoding="utf-8") as out:
    out.write(response)

# ==========================================
# PRINT
# ==========================================

print("\n====================================")
print("FINAL ARCHITECTURE REPORT")
print("====================================\n")

print(response)

print(f"\nSaved: {output_file}")