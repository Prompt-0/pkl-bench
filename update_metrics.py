import re

with open("paper/pkl_bench_paper.tex", "r") as f:
    tex = f.read()

# Update Task 1
tex = tex.replace("accuracy of 0.5442", "accuracy of 0.4580")
tex = tex.replace("Log-Loss: 0.9597", "Log-Loss: 1.1420")
tex = tex.replace("Log-Loss 0.9597", "Log-Loss 1.1420")
tex = tex.replace("0.5442 & 0.2484", "0.4580 & 0.2200") # Need to be careful here if table format changed
tex = re.sub(r"Gradient Boosting.*?& 0\.5442 & 0\.2484 & 0\.9597", r"Gradient Boosting & 0.4580 & 0.2200 & 1.1420", tex)
tex = re.sub(r"Logistic Regression.*?& 0\.5188 & 0\.2274 & 1\.0626", r"Logistic Regression & 0.4428 & 0.1915 & 1.1487", tex)
tex = re.sub(r"Majority Class.*?& 0\.4770 & 0\.1292 & 18\.8520", r"Majority Class & 0.3852 & 0.1112 & 22.1580", tex)

# Update Task 2
tex = re.sub(r"Logistic Leverage & Brier: 0.2195 & ECE: 0.1171 & Log-Loss: 0.6294", r"Logistic Leverage & Brier: 0.2422 & ECE: 0.0591 & Log-Loss: 0.6775", tex)
tex = re.sub(r"\\textbf{Calibrated GBDT} & \\textbf{Brier: 0.1858} & \\textbf{ECE: 0.1495} & \\textbf{Log-Loss: 0.5562}", r"\\textbf{Calibrated GBDT} & \\textbf{Brier: 0.1931} & \\textbf{ECE: 0.1616} & \\textbf{Log-Loss: 0.5734}", tex)
tex = tex.replace("Brier score from 0.2195 to 0.1858", "Brier score from 0.2422 to 0.1931")
tex = tex.replace("(ECE) of 0.1495", "(ECE) of 0.1616")

# Update Task 4
tex = tex.replace("P. Narwal (+470.3)", "P. Narwal (+455.6)")

with open("paper/pkl_bench_paper.tex", "w") as f:
    f.write(tex)

with open("README.md", "r") as f:
    md = f.read()

md = md.replace("0.5442", "0.4580")
md = md.replace("+470.3", "+455.6")

with open("README.md", "w") as f:
    f.write(md)
