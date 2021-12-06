import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go

from src.config_file import Params


PAGE_TITLE = "Walmart sales forecasting"
PAGE_ICON = "https://www.aacc.fr/sites/default/files/styles/logo/https/ucarecdn.com//1033ec06-23ee-4ee6-b583-87f191f58308/type.png?itok=Z0q9Mgu5"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")


st.image("images/barre_eps.PNG", width=400)


st.sidebar.image("images/epsilonlogo.png", width=200)
st.sidebar.header("Prévision des ventes Walmart")


st.sidebar.markdown("---")
st.sidebar.write("Décembre 2021")


# @st.cache
def load_data():
    return joblib.load("outputs/20211203_dict_results.dat")

def load_mape_dict():
    return joblib.load("outputs/20211203_dict_mape.dat")

# @st.cache
def load_prepared_data():
    return pd.read_csv("outputs/data_prepared.csv", parse_dates=["time"])


prepared_data = load_prepared_data()

dictframe = load_data()
dictmape = load_mape_dict()

columns = dictframe.keys()

choice = st.selectbox("Choisir un store", columns)

# fig = plotNode(
#     dictframe=dictframe,
#     column=choice,
#     h=Params.N_FUTURE_WEEKS,
#     xlabel="time",
#     ylabel=choice,
#     uncertainty=True,
# )

# st.pyplot(fig=fig)

df_choice = (
    dictframe[choice]
    .assign(ds=lambda x:pd.to_datetime(x["ds"]))
    .set_index("ds")
    .loc[Params.SPLIT_DATE :]
    )

fig = go.Figure()


fig.add_trace(
    go.Line(x=prepared_data["time"], y=prepared_data[choice], name="Observed")
)


fig.add_trace(go.Line(x=df_choice.index, y=df_choice["yhat"].values, name="Predicted",))

fig.update_layout(height=500, width=1000)

st.metric("MAPE", f"{round(dictmape[choice]*100,2)}%")

st.plotly_chart(fig)

