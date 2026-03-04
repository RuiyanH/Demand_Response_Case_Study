## Demand Response Event Analysis


### Project structure 

The main analysis lives in `analysis.ipynb`, which includes: baseline calculation, exploratory data analysis/visualization, and financial results.

Reusable Python modules live in `src/`: 
- `config.py` holds event relevant constants. 
- `data_loader.py` handles csv reading, timezone conversion, unit conversion, and hourly resampling. 
- `baseline_model.py` computes the 10of10 and FSL baselines and their respective hourly performance for each site.

`data/raw/` stores csv files, each with 15-minute interval kWh readings May–June 2022 for each site. `data/ref/gt.csv` contains ground-truth performance values used for validation.

Generated results are under `outputs/`, including tables and graphics. 


### How to run:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```