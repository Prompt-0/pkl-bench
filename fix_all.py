import re
import json

# 1. Update DATASHEET.md
datasheet = """# PKL-Bench: Datasheet for Dataset

This datasheet follows the framework established by Gebru et al. (2021).

## 1. Motivation
**For what purpose was the dataset created?**
To provide a standardized machine learning benchmark for the Pro Kabaddi League (PKL), addressing the lack of unified play-by-play datasets in contact evasion sports.

**Who created the dataset?**
The structured ML benchmark was engineered by **Ritesh Dobhal** (ritesh2005dobhal@gmail.com).

**Who funded the creation of the dataset?**
Open scientific research initiative.

## 2. Composition
**What do the instances that comprise the dataset represent?**
The dataset contains 1,060 match records and 90,644 discrete raid events across Seasons 1-10 of the PKL.

**Are there any errors, sources of noise, or redundancies?**
Yes. As this dataset is derived from upstream official sources (via `kabaddiPy`), early seasons (particularly Season 1) contain historical recording errors. Play-by-play running scores occasionally decrease, and some official final scores do not perfectly reconcile with the event logs. The benchmark preserves these historical anomalies identically to the source data.

## 3. Collection Process
**How was the data acquired?**
The raw JSON data was acquired from the open-source `kabaddiPy` package, which originally scraped official PKL feeds. PKL-Bench transforms these raw nested JSONs into tabular formats, fixes clock representations, filters non-raid events, and establishes train/test splits.

## 4. Uses
**What tasks is the dataset designed for?**
Raid outcome prediction, dynamic win probability modeling, and pre-match outcome forecasting.

## 5. Distribution
**License:** GNU General Public License v2.0 (GPL-2.0).
"""
with open("docs/DATASHEET.md", "w") as f:
    f.write(datasheet)

# 2. Update .zenodo.json and datapackage.json
def update_json_file(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        
        # Change 103,176 to 90,644
        if "description" in data:
            data["description"] = data["description"].replace("103,176", "90,644")
        
        # Fix License to GPL-2.0
        if "licenses" in data:
            data["licenses"] = [{"id": "GPL-2.0"}]
        elif "license" in data:
            if isinstance(data["license"], dict):
                data["license"]["name"] = "GPL-2.0"
            else:
                data["license"] = "GPL-2.0"

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    except FileNotFoundError:
        pass

update_json_file(".zenodo.json")
update_json_file("datapackage.json")
update_json_file("pkl_bench/datapackage.json")

# 3. Update __init__.py, CONTRIBUTING.md
for fn in ["pkl_bench/__init__.py", "CONTRIBUTING.md", "pkl_bench/loader.py"]:
    try:
        with open(fn, "r") as f:
            text = f.read()
        text = text.replace("103,176", "90,644")
        with open(fn, "w") as f:
            f.write(text)
    except FileNotFoundError:
        pass

# 4. Update README.md
with open("README.md", "r") as f:
    rmd = f.read()

# Fix badges
rmd = rmd.replace("License-CC%20BY%204.0-lightgrey", "License-GPL%202.0-blue")

# Fix numbers in README
rmd = rmd.replace("66,692", "67,181")
rmd = rmd.replace("11,858", "11,642")
rmd = rmd.replace("12,094", "11,821")
rmd = rmd.replace("0.4580", "0.4515")
rmd = rmd.replace("1.1420", "1.1451")
rmd = rmd.replace("0.6838", "0.6838") # task 3 acc
rmd = rmd.replace("0.7673", "0.7673") # task 3 auc
rmd = rmd.replace("+455.6", "+431.2")

with open("README.md", "w") as f:
    f.write(rmd)

