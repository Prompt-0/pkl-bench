# PKL-Bench: Datasheet for Dataset

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
The dataset contains 1,060 match records and 90,644 discrete raid events across Seasons 1-10 of the PKL. The splits are standardized chronologically: Train (S1-S8) with 67,181 raids, Validation (S9) with 11,642 raids, and Test (S10) with 11,821 raids.

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
