import os
from collections import defaultdict

def group_by_package(summary_dir):

    grouped = defaultdict(list)

    for file in os.listdir(summary_dir):

        if not file.endswith(".txt"):
            continue

        # ==========================================
        # DEFAULT PACKAGE
        # ==========================================

        package = "capacity_core"

        # ==========================================
        # SUBPACKAGE DETECTION
        # ==========================================

        if "preemption_" in file:
            package = "preemption"

        elif "allocator_" in file:
            package = "allocator"

        elif "placement_" in file:
            package = "placement"

        elif "policy_" in file:
            package = "policy"

        elif "conf_" in file:
            package = "conf"

        elif "queuemanagement_" in file:
            package = "queuemanagement"

        grouped[package].append(
            os.path.join(summary_dir, file)
        )

    return grouped