from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "census_raw.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_PATH)

# Remove index-only column
df = df.drop(columns=["Unnamed: 0"])

# Clean names
df["First Name"] = df["First Name"].astype(str).str.strip().replace("", "Unknown")
df["Surname"] = df["Surname"].astype(str).str.strip()
df["Surname"] = df.groupby(["Street", "House Number"])["Surname"].transform(
    lambda x: x.replace("", np.nan).ffill().bfill()
)

# Clean age
df["Age"] = df["Age"].astype(str).str.replace("twenty eight", "28")
df["Age"] = pd.to_numeric(df["Age"], errors="coerce").round().astype("Int64")
age_mode = df.loc[
    (df["Relationship to Head of House"] == "Son") & (df["Occupation"] == "Child"), "Age"
].mode()[0]
df["Age"] = df["Age"].fillna(age_mode)

# Standardise gender
gender_map = {
    "M": "Male", "m": "Male", "male": "Male",
    "F": "Female", "f": "Female", "female": "Female"
}
df["Gender"] = df["Gender"].astype(str).str.strip().replace(gender_map)
df["Gender"] = df["Gender"].replace("", "Female")

# Clean occupation
df["Occupation"] = df["Occupation"].astype(str).str.strip().replace("", "Unknown")
df["Occupation"] = df["Occupation"].replace(["sum", "make", "land", "copy"], "Unknown")
df.loc[
    (df["Age"] > 65) & df["Occupation"].str.contains("Unemployed", na=False),
    "Occupation"
] = "Retired"

# Clean infirmity
df["Infirmity"] = df["Infirmity"].astype("string").str.strip().replace("", pd.NA)
df["Infirmity"] = df["Infirmity"].fillna("None")

# Clean house numbers
df["House Number"] = df["House Number"].astype(str).str.replace("Two", "2")
df["House Number"] = pd.to_numeric(df["House Number"], errors="coerce").astype("int64")

# Clean marital status
marital_map = {"S": "Single", "D": "Divorced", "M": "Married", "W": "Widowed"}
df["Marital Status"] = df["Marital Status"].replace(marital_map)
df.loc[df["Age"] < 18, "Marital Status"] = "N/A"

# Clean religion
religion_map = {
    "Nope": "No Religion",
    "Undecided": "No Religion",
    "Agnostic": "No Religion",
    "Jedi": "Other",
    "Housekeeper": "Other",
    "Pagan": "Other",
    "Catholic": "Christian",
    "Methodist": "Christian",
    "Orthodoxy": "Christian"
}
df["Religion"] = df["Religion"].replace(religion_map)

household_religion = df.groupby(["House Number", "Street"])["Religion"].transform(
    lambda x: x.dropna().iloc[0] if x.dropna().nunique() == 1 else "No Religion"
)
df["Religion"] = df["Religion"].fillna(household_religion).fillna("No Religion")

# Correct invalid household heads
df.loc[
    (df["Relationship to Head of House"] == "Head") & (df["Age"] < 18),
    "Relationship to Head of House"
] = np.nan

for _, group in df.groupby(["Street", "House Number"]):
    if (group["Relationship to Head of House"] == "Head").any():
        continue

    adults = group[group["Age"] >= 18]
    if not adults.empty:
        df.loc[adults["Age"].idxmax(), "Relationship to Head of House"] = "Head"

family_surname = df.groupby(["Street", "House Number"])["Surname"].transform("first")
missing_relationship = df["Relationship to Head of House"].isna()

df.loc[missing_relationship & (df["Age"] < 18) & (df["Surname"] == family_surname) &
       (df["Gender"] == "Male"), "Relationship to Head of House"] = "Son"

df.loc[df["Relationship to Head of House"].isna() & (df["Age"] < 18) &
       (df["Surname"] == family_surname) & (df["Gender"] == "Female"),
       "Relationship to Head of House"] = "Daughter"

df.loc[df["Relationship to Head of House"].isna() & (df["Age"] < 18),
       "Relationship to Head of House"] = "Child"

df.loc[df["Relationship to Head of House"].isna() & (df["Age"] >= 18),
       "Relationship to Head of House"] = "Lodger"

output_path = PROCESSED_DIR / "census_cleaned.csv"
df.to_csv(output_path, index=False)

print("Raw records:", 9543)
print("Cleaned records:", len(df))
print("Remaining missing values:", int(df.isna().sum().sum()))
print("Cleaned dataset saved to:", output_path)
