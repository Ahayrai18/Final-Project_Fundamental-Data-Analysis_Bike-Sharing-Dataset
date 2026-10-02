# Bike Sharing Dataset Analysis 🚲

An exploratory data analysis project using the **Bike Sharing Dataset** from Capital Bikeshare in Washington, D.C. The project looks at hourly and daily bike rental patterns from **1 January 2011 to 31 December 2012**, with a focus on usage by time, weather, season, and customer type.

The project includes a fully executed Jupyter Notebook for data cleaning and analysis, plus an interactive Streamlit dashboard for exploring the results.

> **Note:** This is a descriptive analysis project. It uses aggregation, descriptive statistics, visualization, correlation, and manual grouping/binning. No machine learning model is used.

## Business Questions

The analysis was built around three practical questions:

1. **Peak rental hours**  
   At what time does average hourly rental demand peak on working days compared with weekends and holidays, and what percentage of users at those peak hours are registered users?

2. **Weather and seasonal effects**  
   How much does average daily rental demand change during misty/cloudy and light rain/snow conditions compared with clear weather, and which season has the highest and lowest average daily rentals?

3. **Year-over-year growth**  
   How much did total rentals grow from 2011 to 2012, which month had the highest and lowest growth, and how did the share of casual users change?

### Additional analysis

The project also includes manual grouping/binning for:

- Time-of-day segments
- Temperature ranges in 5°C intervals
- Daily demand tiers

These groups are used to turn the raw hourly/daily data into simpler operational patterns that are easier to interpret.

## Dataset

The project uses the **Bike Sharing Dataset**, containing bike rental records from the Capital Bikeshare system in Washington, D.C. for 2011–2012.

### Dataset files

The original dataset contains two main files:

| File | Description | Rows |
|---|---|---:|
| `day.csv` | Daily bike rental records | 731 |
| `hour.csv` | Hourly bike rental records | 17,379 |

The hourly dataset contains an additional `hr` column that records the hour of the day.

### Data source

- [Bike Sharing Dataset – Google Drive](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view?usp=sharing)
- [Bike Sharing Dataset – Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)

The dataset is commonly known as the **UCI Bike Sharing Dataset** and contains Capital Bikeshare rental information together with calendar and weather variables.

## Project Results

The following findings are based on the complete 2011–2012 dataset after the cleaning process in `notebook.ipynb`.

### 1. Peak rental hours

Working days show a clear two-peak commuting pattern:

| Day group | Peak hour | Average rentals/hour | Registered share |
|---|---:|---:|---:|
| Working days | 08:00 | 473 | 95.3% |
| Working days | 17:00 | 524 | 89.2% |
| Weekends & holidays | 13:00 | 373 | 63.4% |

A total of **58% of working-day rentals** occur during the selected commuting hours (07:00–09:59 and 16:00–19:59).

This shows a clear difference in usage patterns: working days are dominated by commuting peaks, while weekends and holidays have a broader midday pattern.

### 2. Weather and season

Compared with clear weather:

| Weather condition | Mean rentals/day | Change vs. clear weather |
|---|---:|---:|
| Clear | 4,877 | — |
| Misty / cloudy | 4,036 | -17.2% |
| Light rain / snow | 1,803 | -63.0% |

The analysis also shows a strong seasonal difference:

| Season | Mean rentals/day |
|---|---:|
| Cold | 2,604 |
| Spring | 4,992 |
| Summer | 5,644 |
| Fall | 4,728 |

Summer has the highest average daily demand, while the cold season has the lowest.

Daily temperature has a positive correlation with total daily rentals of **r = +0.63**. Humidity and wind speed show weaker negative relationships with daily rental demand.

### 3. Growth from 2011 to 2012

| Year | Total rentals | Casual share |
|---|---:|---:|
| 2011 | 1,243,103 | 19.9% |
| 2012 | 2,049,576 | 18.2% |

Total rentals increased by **64.9%** from 2011 to 2012.

Monthly year-over-year growth ranged from:

- **Highest:** March, +157.4%
- **Lowest:** June, +41.3%

The number of registered users grew by **68.4%**, while casual users grew by **50.8%**. As a result, the casual-user share decreased from **19.9% to 18.2%**.

## Data Cleaning

The notebook follows a complete data-wrangling process before the exploratory analysis.

### 1. Load and inspect the source data

Both `day.csv` and `hour.csv` are loaded into pandas DataFrames and checked for structure, data types, missing values, duplicates, and consistency.

### 2. Validate daily and hourly totals

The project checks whether the daily totals in `day.csv` match the sum of hourly rentals in `hour.csv`.

The validation found:

- Missing values in the original CSV tables: **0**
- Duplicate rows: **0**
- `cnt = casual + registered`: **True**
- Days where `day.csv` does not match the aggregated `hour.csv`: **0**

### 3. Complete the hourly timeline

The expected period contains:

```text
731 days × 24 hours = 17,544 hourly records
```

The original `hour.csv` contains **17,379 rows**, leaving **165 missing hourly records (0.94%)**.

The notebook reconstructs the full hourly time index. Missing hourly records are treated as hours with zero recorded rentals, based on the observed consistency with the daily totals.

After completion, the cleaned hourly table contains **17,544 rows** and the total number of rentals remains **3,292,679**, matching the daily dataset.

### 4. Correct the season labels

The original numeric season labels are not interpreted literally from the documentation alone. The notebook checks the month distribution and temperature patterns, then maps the labels as:

| Original code | Project label | Approximate months |
|---:|---|---|
| 1 | Cold | Dec–Mar |
| 2 | Spring | Mar–Jun |
| 3 | Summer | Jun–Sep |
| 4 | Fall | Sep–Dec |

This mapping is used consistently in the notebook and dashboard.

### 5. Convert normalized weather variables

Several weather variables in the original dataset are normalized to a 0–1 range. The notebook converts them back into more readable units:

- Temperature → °C
- Feeling temperature → °C
- Humidity → %
- Wind speed → km/h

### 6. Handle suspicious zero values

The notebook identifies:

- `windspeed = 0` in **2,180 hourly records (12.5%)**
- `hum = 0` in **22 hourly records** on 10 March 2011

These zeros are treated as missing-like values rather than physical measurements and are filled using the surrounding daily/interpolated values described in the notebook.

### 7. Review outliers

An IQR-based check flags **505 hourly records (2.9%)** above the upper fence. About **86%** of these observations occur during commuting hours.

The notebook keeps these observations because they are consistent with genuine high-demand periods rather than automatically removing them as data errors.

## Exploratory Analysis

### Hourly demand

The hourly analysis compares:

- Working days
- Weekends and holidays
- Hour of day
- Registered users
- Casual users

The main pattern is a pair of commuting peaks on working days and a midday peak on weekends and holidays.

### Weather and season

The project compares average daily rentals by:

- Weather condition
- Season
- Temperature
- Humidity
- Wind speed

The weather analysis shows that poor weather conditions are associated with lower average rental demand.

### Yearly and monthly growth

The project compares 2011 and 2012 using:

- Total rentals
- Monthly rental totals
- Year-over-year monthly growth
- Registered-user growth
- Casual-user growth

The analysis also notes that very large growth percentages at the beginning of 2012 are partly influenced by the lower 2011 baseline.

## Manual Grouping / Binning

No machine learning is used for the additional analysis. The notebook uses `pandas.cut()` to create simple, manually defined groups.

### 1. Time segments

The 24 hours are divided into five operational windows:

| Segment | Hours |
|---|---|
| Early morning | 00–05 |
| Morning | 06–09 |
| Afternoon | 10–15 |
| Evening | 16–19 |
| Night | 20–23 |

For working days, the morning and evening segments account for approximately **60%** of rentals.

For weekends and holidays, the afternoon segment becomes the dominant period with approximately **47%** of rentals.

### 2. Temperature bins

Temperature is grouped into 5°C ranges:

```text
<0°C
0–5°C
5–10°C
10–15°C
15–20°C
20–25°C
25–30°C
30–35°C
≥35°C
```

The highest average hourly rental count is found in the **30–35°C** range, at around **331 rentals/hour**.

The lowest average is below **0°C**, at around **56 rentals/hour**.

Hours below 10°C average about **68% fewer rentals** than the best-performing temperature bin.

### 3. Daily demand tiers

Daily rental counts are grouped into three simple tiers:

| Tier | Daily rentals |
|---|---:|
| Low | < 3,000 |
| Medium | 3,000–6,000 |
| High | > 6,000 |

The boundaries were chosen close to the first and third quartiles of daily demand:

- Q1 ≈ 3,152
- Q3 ≈ 5,956

Distribution across all days:

- Low: **23.5%**
- Medium: **51.8%**
- High: **24.6%**

Seasonal demand differs considerably. About **41.5% of summer days** fall into the high-demand tier, while only **2.8% of cold-season days** do.

On light rain/snow days, about **90.5%** of days fall into the low-demand tier and none fall into the high-demand tier.

## Dashboard

The project includes an interactive Streamlit dashboard located at:

```text
 dashboard/dashboard.py
```

The dashboard reads the cleaned dataset from:

```text
 dashboard/main_data.csv
```

### Filters

The sidebar provides:

- Date range
- Season
- Daily weather condition

### Dashboard sections

#### 1 · Hour

Shows:

- Average hourly rental profile
- Working-day vs. weekend/holiday comparison
- Peak commuting hours
- Registered vs. casual share at peak hours

#### 2 · Weather & Season

Shows:

- Daily rentals by weather condition
- Daily rentals by season
- Difference from clear-weather demand

#### 3 · Growth

Shows:

- Year-over-year growth
- Monthly growth
- Registered and casual user growth
- Changes in casual-user share

#### 4 · Advanced Analysis

Shows:

- Time-of-day grouping
- Temperature bins
- Daily demand tiers
- Operational interpretation of the manual groups
- CSV download of the filtered daily data

## Project Structure

```text
Submission_Raihan Muzhaffar Athallah_Bike Sharing Dataset/
├── dashboard/
│   ├── dashboard.py          # Streamlit dashboard
│   └── main_data.csv         # Cleaned hourly dataset generated by the notebook
├── data/
│   ├── day.csv               # Original daily dataset
│   └── hour.csv              # Original hourly dataset
├── .streamlit/
│   └── config.toml           # Streamlit configuration/theme
├── notebook.ipynb            # Full data cleaning, EDA, visualization, and analysis
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── url.txt                   # Deployed dashboard URL
└── .gitignore                # Files excluded from Git
```

## Requirements

- Python 3.11
- pandas >= 2.0
- NumPy >= 1.24
- Matplotlib >= 3.7
- Streamlit >= 1.30

The exact dependencies are listed in `requirements.txt`.

## Local Setup

### Option 1 — Anaconda

Create and activate the environment:

```bash
conda create --name main-ds python=3.11
conda activate main-ds
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Option 2 — Python virtual environment

Open a terminal in the project root:

```bash
cd "Submission_Raihan Muzhaffar Athallah_Bike Sharing Dataset"
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Notebook

Open `notebook.ipynb` in Jupyter Notebook, JupyterLab, VS Code, or Google Colab.

For local Jupyter:

```bash
pip install jupyter
jupyter notebook
```

Run the notebook from the project root so the relative path to `data/` works correctly.

The notebook will:

1. Load `day.csv` and `hour.csv`.
2. Assess data quality.
3. Complete the hourly timeline.
4. Clean and transform the weather variables.
5. Create derived columns for analysis.
6. Perform exploratory analysis.
7. Generate explanatory visualizations.
8. Run the manual grouping/binning analysis.
9. Save the cleaned hourly data to `dashboard/main_data.csv`.

## Run the Streamlit Dashboard

From the project root, run:

```bash
streamlit run dashboard/dashboard.py
```

Streamlit will display the local dashboard URL, normally:

```text
http://localhost:8501
```

Running the command from the project root is recommended because Streamlit Community Cloud also initializes the application from the repository root.

## Deploy to Streamlit Community Cloud

The project structure is already prepared for deployment.

### 1. Push the project to GitHub

The GitHub repository should contain the project root itself, with `requirements.txt` and `.streamlit/config.toml` available from the repository root.

### 2. Open Streamlit Community Cloud

Go to:

https://share.streamlit.io/

Create a new app and select:

```text
Repository : <your GitHub repository>
Branch     : main
Main file  : dashboard/dashboard.py
```

Then click **Deploy**.

Streamlit Community Cloud supports an entrypoint file inside a subdirectory, while the repository root remains the working directory. The `.streamlit/config.toml` file stays at the repository root.

After the app is deployed, place its public URL in `url.txt`.

## Repository Notes

The notebook is the source of the cleaned dataset used by the dashboard. If the raw data or cleaning logic changes, rerun the notebook and update `dashboard/main_data.csv` before deploying the dashboard again.

The Streamlit app reads the cleaned CSV relative to the dashboard file, while deployment runs from the repository root. Keeping the current directory structure intact avoids path-related deployment issues.

## Limitations

- The dataset covers only 2011–2012 and therefore describes historical demand rather than current bike-sharing usage.
- The analysis is descriptive and does not establish causal relationships.
- The large March 2012 year-over-year growth rate is partly affected by the low 2011 baseline.
- Some hourly records are reconstructed to complete the time index.
- Several weather variables in the original data are normalized and require conversion before interpretation.
- The season labels are remapped based on the observed month and temperature patterns in the dataset.
- Manual bins are analytical convenience groups, not official transportation standards.
- The analysis does not use predictive machine learning.

## Author

**Raihan Muzhaffar Athallah**

Final Project — Fundamental Data Analysis
