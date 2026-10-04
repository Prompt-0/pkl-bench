import re

with open("paper/pkl_bench_paper.tex", "r") as f:
    tex = f.read()

# Fix Abstract garbled sentence
tex = tex.replace("(PKL), Derived from the \\texttt{kabaddiPy} package \\cite{lalwani2024kabaddipy}, which sources from official feeds, PKL-Bench harmonizes 1,060 matches", 
                  "(PKL). Derived from the \\texttt{kabaddiPy} package \\cite{lalwani2024kabaddipy} (which aggregates official feeds), PKL-Bench harmonizes 1,060 matches")

# Fix splits
tex = tex.replace("66,692 raid events", "67,181 raid events")
tex = tex.replace("11,858 raid events", "11,642 raid events")
tex = tex.replace("12,094 raid events", "11,821 raid events")

# Fix Task 1 metrics
tex = re.sub(r"Gradient Boosting.*?& 0\.4580 & 0\.2200 & 1\.1420", r"Gradient Boosting & 0.4515 & 0.2136 & 1.1451", tex)
tex = re.sub(r"Logistic Regression.*?& 0\.4428 & 0\.1915 & 1\.1487", r"Logistic Regression & 0.4420 & 0.1906 & 1.1496", tex)
tex = re.sub(r"Majority Class.*?& 0\.3852 & 0\.1112 & 22\.1580", r"Majority Class & 0.3852 & 0.1112 & 22.1580", tex)
tex = tex.replace("accuracy of 0.4580", "accuracy of 0.4515")
tex = tex.replace("Log-Loss: 1.1420", "Log-Loss: 1.1451")
tex = tex.replace("Log-Loss 1.1420", "Log-Loss 1.1451")

# Fix Task 2 metrics
tex = re.sub(r"Logistic Leverage.*?& Brier: 0\.2422 & ECE: 0\.0591 & Log-Loss: 0\.6775", r"Logistic Leverage & Brier: 0.2263 & ECE: 0.0972 & Log-Loss: 0.6438", tex)
tex = re.sub(r"\\textbf{Calibrated GBDT}.*?& \\textbf{Brier: 0\.1931} & \\textbf{ECE: 0\.1616} & \\textbf{Log-Loss: 0\.5734}", r"\\textbf{Calibrated GBDT} & \\textbf{Brier: 0.1798} & \\textbf{ECE: 0.1219} & \\textbf{Log-Loss: 0.5409}", tex)
tex = tex.replace("Brier score from 0.2422 to 0.1931", "Brier score from 0.2263 to 0.1798")
tex = tex.replace("(ECE) of 0.1616", "(ECE) of 0.1219")

# Fix text praising GBDT ECE
tex = tex.replace("achieves an Expected Calibration Error (ECE) of 0.1219 while substantially improving Brier score", "sacrifices some expected calibration error (ECE 0.1219 vs 0.0972) while substantially improving the Brier score")

# Fix Task 3 metrics
tex = tex.replace("Acc: 0.7059", "Acc: 0.6838")
tex = tex.replace("AUC: 0.7707", "AUC: 0.7673")
tex = tex.replace("Margin MAE: 9.23", "Margin MAE: 9.19")

# Fix Task 4 metrics
tex = tex.replace("P. Narwal (+431.2)", "P. Narwal (+431.22)")

# Fix Figure 1 Caption and Sec 2.3
fig1_caption_old = r"\caption{Empirical distributions of raid outcomes (left) and the non-linear relationship between active defender count and super tackle probability (right), illustrating the ``Phase Transitions'' of defensive leverage.}"
fig1_caption_new = r"\caption{Empirical distributions of raid outcomes (left) and the raid success rate over match elapsed time (right), illustrating the degradation of raid efficiency as matches progress.}"
tex = tex.replace(fig1_caption_old, fig1_caption_new)

sec23_old = r"Specifically, we define \textit{Defensive Phase Transitions} based on the active defender count ($N_{def} \in [1, 7]$). As illustrated in Figure \ref{fig:fig1}, the probability of a Super Tackle is empirically zero for $N_{def} > 3$, while bonus point eligibility rigidly activates at $N_{def} \ge 6$."
sec23_new = r"Specifically, we analyze \textit{Raid Efficiency Degradation} based on match elapsed time. As illustrated in Figure \ref{fig:fig1}, the probability of a successful raid empirically degrades as the match progresses into the second half, likely due to defensive adaptation and physical fatigue."
tex = tex.replace(sec23_old, sec23_new)

with open("paper/pkl_bench_paper.tex", "w") as f:
    f.write(tex)

