import pandas as pd

REQUIRED = {"month", "department", "category", "actual", "budget"}

def validate(frame):
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    df = frame[["month", "department", "category", "actual", "budget"]].copy()
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m-%d", errors="raise")
    if df["month"].dt.day.ne(1).any():
        raise ValueError("Month must start on day 1")
    if df["department"].isna().any() or df["department"].astype(str).str.strip().eq("").any():
        raise ValueError("Invalid department")
    if not df["category"].isin(["revenue", "expense"]).all():
        raise ValueError("Invalid category")
    for col in ("actual", "budget"):
        df[col] = pd.to_numeric(df[col], errors="raise")
        if df[col].isna().any() or not df[col].map(lambda x: float("-inf") < x < float("inf")).all() or df[col].lt(0).any():
            raise ValueError(f"Invalid {col}")
    if df.duplicated(["month", "department", "category"]).any():
        raise ValueError("Duplicate rows")
    return df.sort_values("month").reset_index(drop=True)

def monthly(df):
    signed = df.assign(
        actual_signed=df.actual.where(df.category.eq("revenue"), -df.actual),
        budget_signed=df.budget.where(df.category.eq("revenue"), -df.budget))
    return signed.groupby("month", as_index=False)[["actual_signed", "budget_signed"]].sum().rename(
        columns={"actual_signed": "operating_result", "budget_signed": "budget_result"})

def runway(cash, monthly_net_flow):
    if cash < 0:
        raise ValueError("Cash cannot be negative")
    return cash / -monthly_net_flow if monthly_net_flow < 0 else None

def scenario(df, revenue_change, expense_change):
    revenue = df.loc[df.category.eq("revenue"), "actual"].sum()
    expense = df.loc[df.category.eq("expense"), "actual"].sum()
    return revenue * (1 + revenue_change) - expense * (1 + expense_change)

def insights(df):
    df = validate(df)
    trend = monthly(df)
    latest = trend.iloc[-1]
    delta = latest.operating_result - latest.budget_result
    notes = [f"Latest operating result: ${latest.operating_result:,.0f}; budget variance: ${delta:+,.0f}."]
    expenses = df[df.category.eq("expense")].copy()
    if not expenses.empty:
        expenses["overspend"] = expenses.actual - expenses.budget
        top = expenses.sort_values("overspend", ascending=False).iloc[0]
        if top.overspend > 0:
            notes.append(f"Largest expense overspend: {top.department}, {top.month:%Y-%m}, ${top.overspend:,.0f}.")
    return notes
