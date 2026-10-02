# Titanic Explorer

Explore the Titanic dataset (`seaborn.load_dataset("titanic")`):
clean it, analyze survival rates, and save charts.

## Project layout
- `main.py` – runs the whole pipeline
- `titanic/cleaning.py` – load and clean the data
- `titanic/analysis.py` – survival rates and summary statistics
- `titanic/charts.py` – save charts to `outputs/`
- `tests/` – pytest tests

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python main.py   # prints a report and writes PNGs to outputs/
pytest -v        # runs the tests
```
