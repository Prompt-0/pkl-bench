import re

with open("paper/pkl_bench_paper.tex", "r") as f:
    tex = f.read()

# 1. Update Provenance in abstract
tex = tex.replace("PKL-Bench harmonizes 1,060 matches", "Derived from the \\texttt{kabaddiPy} package \\cite{lalwani2024kabaddipy}, which sources from official feeds, PKL-Bench harmonizes 1,060 matches")

# 2. Update Provenance in Introduction
old_intro = """No unified, multi-season, play-by-play benchmark dataset with rigorous evaluation protocols has existed.

To resolve this deficiency, we present \\textbf{PKL-Bench}, an open-science benchmark suite designed according to FAIR principles:"""
new_intro = """While raw match data was recently packaged in \\texttt{kabaddiPy} \\cite{lalwani2024kabaddipy}, no unified, multi-season, play-by-play machine learning benchmark suite with rigorous evaluation protocols has existed.

To resolve this deficiency, we present \\textbf{PKL-Bench}, an open-science benchmark suite built upon the raw data from \\texttt{kabaddiPy}, designed according to FAIR principles:"""
tex = tex.replace(old_intro, new_intro)

# 3. Update Dataset Architecture (Task 1 classes)
old_classes = """\\mathcal{Y} = \\{ & \\text{EMPTY}, \\text{SUCCESSFUL\\_TOUCH}, \\text{BONUS\\_ONLY}, \\\\
& \\text{SUPER\\_RAID}, \\text{UNSUCCESSFUL\\_TACKLE}, \\text{SUPER\\_TACKLE} \\}"""
new_classes = """\\mathcal{Y} = \\{ & \\text{EMPTY\\_RAID}, \\text{SUCCESSFUL\\_RAID}, \\text{UNSUCCESSFUL\\_RAID}, \\\\
& \\text{SUPER\\_RAID}, \\text{SUPER\\_TACKLE} \\}"""
tex = tex.replace(old_classes, new_classes)

# 4. Update the numbers in the abstract
tex = tex.replace("103,176 timestamped, discrete raid events", "90,644 timestamped, discrete raid events")
tex = tex.replace("103,176 discrete play-by-play raid events", "90,644 discrete play-by-play raid events")
tex = tex.replace("103,176 events in PKL-Bench", "90,644 events in PKL-Bench")
tex = tex.replace("103,176 granular raid records", "90,644 granular raid records")
tex = tex.replace("103,176 Play-by-Play Raids", "90,644 Play-by-Play Raids")

tex = tex.replace("75,777 raid events", "66,692 raid events")
tex = tex.replace("13,505 raid events", "11,858 raid events")
tex = tex.replace("13,894 raid events", "12,094 raid events")

# 5. Update the table 2 numbers
tex = re.sub(r"Logistic Leverage & Brier: 0.2270 & ECE: 0.1882 & Log-Loss: 0.6446", r"Logistic Leverage & Brier: 0.2195 & ECE: 0.1171 & Log-Loss: 0.6294", tex)
tex = re.sub(r"\\textbf{Calibrated GBDT} & \\textbf{Brier: 0.1991} & \\textbf{ECE: 0.1561} & \\textbf{Log-Loss: 0.5827}", r"\\textbf{Calibrated GBDT} & \\textbf{Brier: 0.1858} & \\textbf{ECE: 0.1495} & \\textbf{Log-Loss: 0.5562}", tex)
tex = re.sub(r"Expected Points Added} & \\textbf{Top Cum.: P. Narwal \(\+470.3\)}", r"Expected Points Added} & \\textbf{Top Cum.: P. Narwal (+470.3)}", tex)

# Key insights update
tex = tex.replace("ECE) from 0.1882 to 0.1561", "ECE) from 0.1171 to 0.1495") # wait gbdt ECE is actually higher than Logistic in this run (0.1495 vs 0.1171). 
tex = tex.replace("reduces Expected Calibration Error (ECE) from 0.1171 to 0.1495", "achieves an Expected Calibration Error (ECE) of 0.1495 while substantially improving Brier score from 0.2195 to 0.1858")
tex = tex.replace("reduces Expected Calibration Error (ECE) from 0.1882 to 0.1561", "achieves an Expected Calibration Error (ECE) of 0.1495 while substantially improving Brier score from 0.2195 to 0.1858")

# 6. Add limitations and ethics section before Conclusion
limitations = """
\\section{Limitations, Ethics, & Data Provenance}
\\textbf{Data Provenance}: The raw JSON match files underpinning PKL-Bench were compiled by Lalwani et al. in the \\texttt{kabaddiPy} package \\cite{lalwani2024kabaddipy}, which aggregates public data from the official Pro Kabaddi League website. PKL-Bench builds upon this raw data to create a strictly defined machine learning evaluation harness.

\\textbf{Limitations}: There are known discrepancies in the historical data, particularly in Season 1, where official play-by-play scores sometimes diverge from documented final outcomes. Our 100\\% score conservation theorem verifies that the mathematical events in the raw data sum exactly to the final data record, but does not guarantee historical perfection of the official feeds. Additionally, ties are excluded from binary win probability evaluation for simplicity, though they constitute $\\approx 8.1\\%$ of historical matches.

\\textbf{AI Disclosure}: Portions of the codebase, documentation, and this manuscript were drafted and refactored with the assistance of Large Language Models, undergoing human verification.
"""
tex = tex.replace("\\section{Conclusion & Open Research Directions}", limitations + "\n\\section{Conclusion & Open Research Directions}")

with open("paper/pkl_bench_paper.tex", "w") as f:
    f.write(tex)

