# Titanic Explorer

Explore the Titanic dataset (`seaborn.load_dataset("titanic")`):
clean it, analyze survival rates, and save charts.

## Key findings


## Project layout
- `main.py` – runs the whole pipeline: load → clean → (charts) → report
- `src/load.py` – load the data, save a copy to `data/titanic.csv`, describe it
- `src/clean.py` – fill or remove missing values
- `src/analyze.py` – survival rates and passenger counts
- `src/charts.py` – save one PNG chart per finding to `outputs/`
- `src/report.py` – write the summary report to `outputs/report.txt`
- `tests/` – pytest tests, one file per module

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python3 main.py           # prints the report and saves it to outputs/report.txt
python3 main.py --chart   # same, and also saves PNG charts to outputs/
python3 main.py --help    # lists the options
pytest -v                 # runs the tests
```

## Outputs
Running `main.py` creates these (the `outputs/` folder is not tracked by git):
- `data/titanic.csv` – a copy of the raw dataset
- `outputs/report.txt` – the survival report
- `outputs/1_overall_survival.png` … `outputs/5_survival_by_age_group.png` –
  one chart per finding (only with `--chart`)

## Data cleaning choices
- `age` (177 missing): filled with the median age for the passenger's class
  and sex; an `age_was_missing` column records which ages were filled.
- `deck` (688 missing): dropped; a `has_deck` column records whether it was known.
- `embarked`, `embark_town` (2 missing each): filled with the most common port.
- Age comparisons use recorded ages only, because filled ages are all adult
  medians.
