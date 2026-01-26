import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("死因順位別にみた年次別死亡率（人口10万対）.csv",encoding="cp932")
with st.sidebar:
    option=st.toggle("年別にみる")
    st.subheader("絞り込み条件")
    if option==True:
        year = st.selectbox('年を選んでください',
                          df["年次"].unique())
        df = df[df["年次"]==year]
        rows = []

        for i in range(1, 11):
            rows.append({
                "死因":df[f"第{i}位"].values[0],
                "死亡率":df[f"第{i}位死亡率"].values[0]
                })

        result_df = pd.DataFrame(rows)

        result_df.set_index("死因",inplace=True)

if option==True:
    st.dataframe(result_df,width=800,height=220)
    st.bar_chart(result_df)