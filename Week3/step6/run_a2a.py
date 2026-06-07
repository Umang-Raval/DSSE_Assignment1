import subprocess

A2A_JAR = "arcade_core_A2a.jar"

comparisons = [
    ("LIMBO vs Jina ARC 0.4",
     r"..\..\Week1\Outputs\LIMBO\limbo-100_IL_20_clusters.rsf",
     r"..\Jinaai\Outputs\ARC_0.4_10.rsf"),

    ("LIMBO vs Jina ARC 0.6",
     r"..\..\Week1\Outputs\LIMBO\limbo-100_IL_20_clusters.rsf",
     r"..\Jinaai\Outputs\ARC_0.6_20.rsf"),

    ("LIMBO vs CodeRank ARC 0.4",
     r"..\..\Week1\Outputs\LIMBO\limbo-100_IL_20_clusters.rsf",
     r"..\CodeRankEmbed\Outputs\ARC_0.4_10.rsf"),

    ("LIMBO vs CodeRank ARC 0.6",
     r"..\..\Week1\Outputs\LIMBO\limbo-100_IL_20_clusters.rsf",
     r"..\CodeRankEmbed\Outputs\ARC_0.6_20.rsf"),

    ("ACDC vs Jina ARC 0.4",
     r"..\..\Week1\Outputs\ACDC\output.rsf",
     r"..\Jinaai\Outputs\ARC_0.4_10.rsf"),

    ("ACDC vs Jina ARC 0.6",
     r"..\..\Week1\Outputs\ACDC\output.rsf",
     r"..\Jinaai\Outputs\ARC_0.6_20.rsf"),

    ("ACDC vs CodeRank ARC 0.4",
     r"..\..\Week1\Outputs\ACDC\output.rsf",
     r"..\CodeRankEmbed\Outputs\ARC_0.4_10.rsf"),

    ("ACDC vs CodeRank ARC 0.6",
     r"..\..\Week1\Outputs\ACDC\output.rsf",
     r"..\CodeRankEmbed\Outputs\ARC_0.6_20.rsf"),

    ("Jina ARC 0.4 vs Jina ARC 0.6",
     r"..\Jinaai\Outputs\ARC_0.4_10.rsf",
     r"..\Jinaai\Outputs\ARC_0.6_20.rsf"),

    ("CodeRank ARC 0.4 vs CodeRank ARC 0.6",
     r"..\CodeRankEmbed\Outputs\ARC_0.4_10.rsf",
     r"..\CodeRankEmbed\Outputs\ARC_0.6_20.rsf"),

    ("Jina ARC 0.4 vs CodeRank ARC 0.4",
     r"..\Jinaai\Outputs\ARC_0.4_10.rsf",
     r"..\CodeRankEmbed\Outputs\ARC_0.4_10.rsf"),

    ("Jina ARC 0.6 vs CodeRank ARC 0.6",
     r"..\Jinaai\Outputs\ARC_0.6_20.rsf",
     r"..\CodeRankEmbed\Outputs\ARC_0.6_20.rsf"),
]

for name, file1, file2 in comparisons:
    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    subprocess.run(
        ["java", "-jar", A2A_JAR, file1, file2],
        check=False
    )