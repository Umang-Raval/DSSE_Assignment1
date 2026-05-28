import json

input_file = "Week3_Group5_nomic_ai_CodeRankEmbed.ipynb"
output_file = "Week3_Group5_nomic_ai_CodeRankEmbed_clean.ipynb"

with open(input_file, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Remove notebook-level widget metadata
if "metadata" in nb and "widgets" in nb["metadata"]:
    del nb["metadata"]["widgets"]

# Remove widget outputs from cells
for cell in nb.get("cells", []):
    if "outputs" in cell:
        cleaned_outputs = []

        for output in cell["outputs"]:
            remove_output = False

            if "data" in output:
                if "application/vnd.jupyter.widget-view+json" in output["data"]:
                    remove_output = True

            if not remove_output:
                cleaned_outputs.append(output)

        cell["outputs"] = cleaned_outputs

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Clean notebook saved as:", output_file)