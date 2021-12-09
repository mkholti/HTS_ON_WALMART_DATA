import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from src.utils import load_data, load_mape_dict
from src.config_file import Params


def prevision_per_store(prepared_data, method="BU"):
    if method == "BU":
        dictframe = load_data("outputs/20211203_dict_results.dat")
        dictmape = load_mape_dict("outputs/20211203_dict_mape.dat")

    if method == "OLS":
        dictframe = load_data("outputs/20211207_dict_results_OLS.dat")
        dictmape = load_mape_dict("outputs/20211207_dict_mape_OLS.dat")

    columns = dictframe.keys()

    choice = st.selectbox(
        "choose all stores, a departement or a combination department x store", columns
    )

    df_choice = (
        dictframe[choice]
        .assign(ds=lambda x: pd.to_datetime(x["ds"]))
        .set_index("ds")
        .loc[Params.SPLIT_DATE :]
    )

    fig = go.Figure()
    fig.add_trace(
        go.Line(x=prepared_data["time"], y=prepared_data[choice], name="Observed")
    )
    fig.add_trace(
        go.Line(x=df_choice.index, y=df_choice["yhat"].values, name="Predicted",)
    )

    fig.update_layout(height=500, width=1000)

    st.metric("MAPE", f"{round(dictmape[choice]*100,2)}%")

    st.plotly_chart(fig)

    col1, col2 = st.columns(2)

    with col1:
        dep_choice = st.selectbox(
            "select a departement", [f"dep{dep_id}" for dep_id in Params.SAMPLE_DEP_ID]
        )
    with col2:
        dep_stores = list(
            filter(lambda x: x.startswith(f"{dep_choice}_store"), columns)
        )
        stores_to_plot = st.multiselect(
            "select stores", dep_stores, default=dep_stores[0]
        )

    if stores_to_plot:
        mape_cols = st.columns(len(stores_to_plot))

        for i, mape_col in enumerate(mape_cols):
            store = stores_to_plot[i]
            with mape_col:
                st.metric(f"MAPE for {store}", f"{round(dictmape[store]*100,2)}%")

        fig2 = go.Figure()
        for store in stores_to_plot:
            df_store = (
                dictframe[store]
                .assign(ds=lambda x: pd.to_datetime(x["ds"]))
                .set_index("ds")
                .loc[Params.SPLIT_DATE :]
            )
            fig2.add_trace(
                go.Line(
                    x=prepared_data["time"],
                    y=prepared_data[store],
                    name=f"Observed for {store}",
                )
            )
            fig2.add_trace(
                go.Line(
                    x=df_store.index,
                    y=df_store["yhat"].values,
                    name=f"Predicted for {store}",
                )
            )

        fig2.update_layout(height=500, width=1000)

        st.plotly_chart(fig2)
