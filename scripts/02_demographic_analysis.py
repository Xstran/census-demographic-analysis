from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "census_cleaned.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError("Run scripts/01_data_cleaning.py first.")

df = pd.read_csv(DATA_PATH)
total_population = len(df)

# ------------------------------------------------------------
# POPULATION AGE STRUCTURE
# ------------------------------------------------------------

age_groups = pd.Series({
    "Under 18": (df["Age"] < 18).sum(),
    "Working age (18-64)": df["Age"].between(18, 64).sum(),
    "65+": (df["Age"] >= 65).sum()
})

plt.figure(figsize=(8, 5))
sns.barplot(x=age_groups.values, y=age_groups.index)
plt.title("Population by Age Group")
plt.xlabel("Population")
plt.ylabel("")
plt.tight_layout()
plt.savefig(RESULTS_DIR / "population_age_groups.png", dpi=300)
plt.close()

# ------------------------------------------------------------
# UNEMPLOYMENT
# ------------------------------------------------------------

working_age = df[df["Age"].between(18, 65)].copy()
working_age["unemployed"] = working_age["Occupation"].str.contains(
    "Unemployed", case=False, na=False
)

overall_unemployment = working_age["unemployed"].mean() * 100

age_bins = [18, 25, 35, 45, 55, 66]
age_labels = ["18-24", "25-34", "35-44", "45-54", "55-65"]
working_age["age_group"] = pd.cut(
    working_age["Age"], bins=age_bins, labels=age_labels, right=False
)

unemployment_by_age = (
    working_age.groupby("age_group", observed=False)["unemployed"].mean() * 100
)

plt.figure(figsize=(8, 5))
sns.lineplot(x=unemployment_by_age.index, y=unemployment_by_age.values, marker="o")
plt.title("Unemployment Rate by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Unemployment Rate (%)")
plt.tight_layout()
plt.savefig(RESULTS_DIR / "unemployment_by_age.png", dpi=300)
plt.close()

# ------------------------------------------------------------
# HOUSEHOLD OCCUPANCY
# ------------------------------------------------------------

household_size = df.groupby(["Street", "House Number"]).size()

plt.figure(figsize=(8, 5))
sns.histplot(household_size, bins=20)
plt.title("Household Occupancy Distribution")
plt.xlabel("People per Household")
plt.ylabel("Number of Households")
plt.tight_layout()
plt.savefig(RESULTS_DIR / "household_occupancy.png", dpi=300)
plt.close()

# ------------------------------------------------------------
# COMMUTER ESTIMATION
# ------------------------------------------------------------

commuter_keywords = [
    "university student", "phd", "engineer", "scientist", "research",
    "consultant", "analyst", "planner", "architect", "surveyor",
    "developer", "lawyer", "solicitor", "finance", "accountant",
    "banker", "doctor", "pharmacist", "lecturer", "professor",
    "manager", "director", "executive", "data", "software",
    "programmer", "marketing", "technician", "specialist", "logistics"
]

non_commuter_keywords = [
    "child", "unemployed", "retired", "unknown", "barista",
    "restaurant", "retail", "shop", "sales assistant", "teacher",
    "care", "maintenance", "librarian", "driver"
]

def classify_commuter(occupation):
    occupation = str(occupation).lower()

    if any(word in occupation for word in non_commuter_keywords):
        return "Non-Commuter"

    if any(word in occupation for word in commuter_keywords):
        return "Commuter"

    return "Unknown"

df["commuter_status"] = df["Occupation"].apply(classify_commuter)
commuter_distribution = df["commuter_status"].value_counts()

plt.figure(figsize=(7, 5))
sns.barplot(x=commuter_distribution.index, y=commuter_distribution.values)
plt.title("Estimated Commuter Status")
plt.xlabel("")
plt.ylabel("Population")
plt.tight_layout()
plt.savefig(RESULTS_DIR / "commuter_estimate.png", dpi=300)
plt.close()

print("Population:", total_population)
print(f"Working-age unemployment rate: {overall_unemployment:.2f}%")
print("Households:", len(household_size))
print("Average household size:", round(household_size.mean(), 2))
print("\nEstimated commuter status:")
print((df["commuter_status"].value_counts(normalize=True) * 100).round(2))
print("\nFigures saved to:", RESULTS_DIR)
