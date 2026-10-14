# AI Financial Intelligence Platform

Interactive CFO dashboard for budget variance, operating performance, cash runway and scenarios.

**Synthetic-data portfolio demonstration.** Automated insights are rules-based, not generative AI. This is not a GAAP income statement.

## Quick start
```bash
pip install -r requirements.txt
streamlit run app.py
```

Input CSV: month (YYYY-MM-DD), department, category (revenue/expense), actual, budget. Values must be nonnegative.

## Tests
```bash
pip install pytest
pytest -q
```

No confidential data or credentials should be uploaded.