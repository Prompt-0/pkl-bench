import re

with open("docs/DATASHEET.md", "r") as f:
    md = f.read()

# Fix numbers
md = md.replace("103,176", "90,644")

# Fix Provenance
md = re.sub(r"The dataset was engineered, harmonized, and verified by \*\*Ritesh Dobhal\*\*(.*?)communities\.", 
            r"The structured benchmark was engineered by **Ritesh Dobhal**\1communities. The raw underlying data is strictly derived from the `kabaddiPy` open-source package, which aggregated historical feeds from the official PKL website.", md)

md = re.sub(r"Open scientific research initiative; self-funded under open-science principles\.",
            r"Open scientific research initiative. Raw data sourcing is credited to the authors of `kabaddiPy`.", md)

with open("docs/DATASHEET.md", "w") as f:
    f.write(md)
