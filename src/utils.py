import joblib
import pandas as pd

# @st.cache
def load_data(f):
    return joblib.load(f)

def load_mape_dict(f):
    return joblib.load(f)

# @st.cache
def load_prepared_data():
    return pd.read_csv("outputs/data_prepared.csv", parse_dates=["time"])