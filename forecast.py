import pandas as pd

def forecast(trend, periods=6):
    if periods < 1 or len(trend) < 2:
        raise ValueError('Need two historical periods and a positive forecast horizon')
    series = trend.sort_values('month')['operating_result'].astype(float)
    slope = (series.iloc[-1] - series.iloc[0]) / (len(series) - 1)
    last = pd.to_datetime(trend['month']).max().to_period('M')
    return pd.DataFrame({'month': [(last + i).to_timestamp() for i in range(1, periods + 1)], 'forecast_result': [float(series.iloc[-1] + slope * i) for i in range(1, periods + 1)]})
