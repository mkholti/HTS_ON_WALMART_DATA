import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from src.utils import load_data, load_mape_dict
from src.config_file import Params


def prevision_per_store(prepared_data, method="BU"):
    if method=="BU":
        dictframe = load_data("outputs/20211203_dict_results.dat")
        dictmape = load_mape_dict("outputs/20211203_dict_mape.dat")

    if method=="OLS":
        dictframe = load_data("outputs/20211207_dict_results_OLS.dat")
        dictmape = load_mape_dict("outputs/20211207_dict_mape_OLS.dat")

    columns = dictframe.keys()

    choice = st.selectbox("choose all stores, a departement or a combination department x store", columns)

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

    