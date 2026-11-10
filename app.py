"""Slim COVID Tracker for Render Free (512 MB). Local CSV, Streamlit charts only."""

from pathlib import Path

import pandas as pd
import streamlit as st

DATE_COLUMN = "dateRep"
DATA_PATH = Path(__file__).parent / "data" / "ecdc_covid_sample.csv"

st.set_page_config(page_title="Covid Tracker", page_icon="🦠", layout="wide")

st.title("Covid Tracker")
st.markdown(
    "Welcome to this simple covid tracker. It tracks reported cases across countries "
    "using a local ECDC sample so the app stays small enough for Render Free (512 MB)."
)
st.caption("Sample data inspired by ECDC daily COVID-19 reporting. For teaching only.")


@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], dayfirst=True)
    return data


data_load_state = st.text("Loading data...")
data = load_data()
data_load_state.text(f"Loaded {len(data)} rows.")

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

st.subheader("World analysis")
world = data.groupby(DATE_COLUMN, as_index=False)[["cases", "deaths"]].sum()
world = world.sort_values(DATE_COLUMN)
world["cumulated_cases"] = world["cases"].cumsum()
world["cases_7d"] = world["cases"].rolling(window=7, min_periods=1).mean()

st.markdown("#### Cumulated cases")
st.line_chart(world.set_index(DATE_COLUMN)["cumulated_cases"])

st.markdown("#### New cases (7-day average)")
st.line_chart(world.set_index(DATE_COLUMN)[["cases", "cases_7d"]])

st.subheader("Country analysis")
countries = sorted(data["countriesAndTerritories"].dropna().unique())
country = st.selectbox("Which country would you like to see?", countries)
country_df = (
    data[data["countriesAndTerritories"] == country]
    .loc[:, [DATE_COLUMN, "cases", "deaths"]]
    .sort_values(DATE_COLUMN)
)
country_df["cases_7d"] = country_df["cases"].rolling(window=7, min_periods=1).mean()

st.markdown(f"#### Cases in {country}")
st.line_chart(country_df.set_index(DATE_COLUMN)[["cases", "cases_7d"]])

st.markdown(f"#### Deaths in {country}")
st.line_chart(country_df.set_index(DATE_COLUMN)["deaths"])

latest = country_df.iloc[-1] if len(country_df) else None
if latest is not None:
    c1, c2 = st.columns(2)
    c1.metric("Latest daily cases", int(latest["cases"]))
    c2.metric("Latest daily deaths", int(latest["deaths"]))
