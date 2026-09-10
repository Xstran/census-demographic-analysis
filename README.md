# Census Demographic Analysis

Data cleaning and demographic analysis of a simulated 2025 census dataset to support local planning and investment decisions.

The project analyses 9,543 population records containing household, demographic, occupation, health and religion information. The dataset is synthetic and was generated to emulate the structure of a census rather than represent real individuals.

## Project Goal

The analysis was designed to answer two practical planning questions:

- What should be developed on an available plot of land?
- Which area of public spending should receive additional investment?

The workflow combines extensive data cleaning with demographic and household analysis to support evidence-based recommendations.

## Key Findings

- Total population: **9,543**
- **23.0%** of residents were under 18.
- **66.6%** were of working age.
- **10.4%** were aged 65 or above.
- Estimated working-age unemployment was **8.47%**.
- Estimated commuters represented **45.58%** of the population.
- The dataset contained **3,332 households**.
- Average household occupancy was approximately **2.86 people**.

## Population Structure

![Population age pyramid](results/population_age_pyramid.png)

The population was dominated by working-age residents, with smaller proportions of children and older residents.

## Employment Analysis

![Unemployment by age](results/unemployment_by_age.png)

![Unemployment by gender](results/unemployment_by_gender.png)

Unemployment varied considerably across age groups, with the overall working-age unemployment rate estimated at 8.47%.

## Household Analysis

![Household occupancy](results/household_occupancy.png)

Household-level analysis was used to examine housing utilisation and population density across the simulated town.

## Commuter Analysis

University students were treated as commuters because the simulated town does not contain a university. Occupation-based rules were also used to estimate whether other residents were likely commuters.

The resulting estimate classified:

- **45.58%** as commuters
- **22.99%** as non-commuters
- **31.43%** as unknown

## Data Cleaning

The raw census contained missing, inconsistent and implausible values. Cleaning included:

- standardising gender and marital-status categories
- correcting textual and invalid age values
- cleaning occupations and household numbers
- handling missing surnames using household information
- standardising religion categories
- resolving missing household relationships
- correcting invalid household heads
- validating remaining missing values

The cleaning pipeline produces a processed dataset automatically rather than storing a second copy in the repository.

## Recommendations

Based on the demographic, commuting, employment and household analysis:

**Development recommendation:** Train station

**Investment recommendation:** Employment and training

## Project Structure

```text
census-demographic-analysis/
├── data/
│   └── raw/
│       └── census_raw.csv
├── results/
│   ├── household_occupancy.png
│   ├── population_age_pyramid.png
│   ├── unemployment_by_age.png
│   └── unemployment_by_gender.png
├── scripts/
│   ├── 01_data_cleaning.py
│   └── 02_demographic_analysis.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
