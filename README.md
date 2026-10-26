# Customer project

An in-progress ZenML training pipeline using the Olist customer dataset.

## Set up on another computer

Use Python 3.14, then run from the project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
zenml login --local
python run_pipeline.py
```

The dataset is stored at `data/olist_customers_dataset.csv`.

Before running on another computer, update the absolute dataset path in
`run_pipeline.py` to match the new location.

This project is still being built; some pipeline steps are placeholders.
