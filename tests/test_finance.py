import pandas as pd
import pytest
from finance import validate, monthly, runway, scenario, insights

@pytest.fixture
def frame():
    return pd.DataFrame([
        {"month": "2026-07-01", "department": "Sales", "category": "revenue", "actual": 120, "budget": 100},
        {"month": "2026-07-01", "department": "Ops", "category": "expense", "actual": 80, "budget": 70},
    ])

def test_monthly(frame):
    result = monthly(validate(frame)).iloc[0]
    assert result.operating_result == 40
    assert result.budget_result == 30

def test_runway():
    assert runway(100, -20) == 5
    assert runway(100, 5) is None

def test_scenario(frame):
    assert scenario(validate(frame), .1, 0) == pytest.approx(52)

def test_insights(frame):
    assert len(insights(frame)) == 2

def test_negative_rejected(frame):
    frame.loc[0, "actual"] = -1
    with pytest.raises(ValueError):
        validate(frame)

def test_duplicate_rejected(frame):
    with pytest.raises(ValueError):
        validate(pd.concat([frame, frame.iloc[[0]]]))
