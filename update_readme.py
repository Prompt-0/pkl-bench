import re

with open("README.md", "r") as f:
    md = f.read()

# Fix numbers
md = md.replace("103,176", "90,644")
md = md.replace("75,777", "66,692")
md = md.replace("13,505", "11,858")
md = md.replace("13,894", "12,094")
md = md.replace("0.5319", "0.5442")
md = md.replace("+633.4", "+470.3")

# Fix Provenance
prov = """## 🌟 Motivation & Provenance
While sports analytics has seen massive open-source contributions in soccer (SoccerNet) and basketball (NBA Play-by-Play), contact evasion sports have been left behind. **PKL-Bench** bridges this gap. 

**Data Provenance**: The raw match data is strictly derived from the excellent `kabaddiPy` open-source package, which aggregated historical feeds from the official PKL website. PKL-Bench transforms these raw nested JSONs into a standardized, tabular machine learning evaluation suite with strict temporal cross-validation."""
md = re.sub(r"## 🌟 Motivation\n.*?(?=\n\n## 📊)", prov, md, flags=re.DOTALL)

# Fix License
lic = """## 📜 License

This dataset and codebase are built upon `kabaddiPy` and are distributed under the **GNU General Public License v2.0 (GPL-2.0)** to comply with the upstream data source and promote open-science."""
md = re.sub(r"## 📜 License\n.*", lic, md, flags=re.DOTALL)

with open("README.md", "w") as f:
    f.write(md)

