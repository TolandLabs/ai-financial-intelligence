import pandas as pd
import pytest
from forecast import forecast

def test_forecast():
    data = pd.DataFrame({'month': ['2026-07-01', '2026-08-01', '2026-09-01'], 'operating_result': [10, 20, 30]})
    assert forecast(data, 2)['forecast_result'].tolist() == pytest.approx([40, 50])

def test_short_history():
    with pytest.raises(ValueError):
        forecast(pd.DataFrame({'month': ['2026-07-01'], 'operating_result': [10]}))
