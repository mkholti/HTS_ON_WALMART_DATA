import streamlit as st
import pandas as pd

from src.config_file import Params
from src.utils_app import prevision_per_store
from src.utils import load_prepared_data


PAGE_TITLE = "Walmart sales forecasting"
PAGE_ICON = "https://www.aacc.fr/sites/default/files/styles/logo/https/ucarecdn.com//1033ec06-23ee-4ee6-b583-87f191f58308/type.png?itok=Z0q9Mgu5"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")


st.image("images/barre_eps.PNG", width=400)


st.sidebar.image("images/epsilonlogo.png", width=200)
st.sidebar.header("Prévision des ventes Walmart")


menu = st.sidebar.radio(
    "méthode:",
    ("BU",
     "OLS",
    ),
)

st.sidebar.markdown("---")
st.sidebar.write("Décembre 2021")


prepared_data = load_prepared_data()

if menu=="BU":
    prevision_per_store(prepared_data, method="BU")

if menu=="OLS":
    prevision_per_store(prepared_data, method="OLS")




