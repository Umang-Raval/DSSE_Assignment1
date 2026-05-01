focus_prefix = "org.apache.hadoop.yarn.server.resourcemanager.scheduler"

with open("output/YARN_full.rsf") as f_in, \
     open("output/YARN_filtered.rsf", "w") as f_out:
    for line in f_in:
        parts = line.strip().split()
        if len(parts) == 3:
            _, src, tgt = parts
            if focus_prefix in src or focus_prefix in tgt:
                f_out.write(line)

print("Filtering done")