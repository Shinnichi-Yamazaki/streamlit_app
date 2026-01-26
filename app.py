import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("死因順位別にみた年次別死亡率（人口10万対）.csv",encoding="cp932")
tab1,tab2=st.tabs(["グラフ・表","数値"])
with st.sidebar:
    
    option=st.selectbox('表示方法を選択してください',
                        ["年別にみる","死因別にみる"])
    st.subheader("絞り込み条件")
    if option=="年別にみる":
        year = st.selectbox('年を選んでください',
                        df["年次"].unique())
        df = df[df["年次"]==year]
        rows = []

        for i in range(1, 11):
            rows.append({
                "死因":df[f"第{i}位"].values[0],
                "死亡率":df[f"第{i}位死亡率"].values[0]
                })

        df = pd.DataFrame(rows)
        df.set_index("死因",inplace=True)
    
    if option=="死因別にみる":
        records = []

        years = df["年次"]

        for i in range(1, 11):
            causes = df[f"第{i}位"]
            rates  = df[f"第{i}位死亡率"]

            for year, cause, rate in zip(years, causes, rates):
                records.append({
                    "年次": year,
                    "死因": cause,
                    "死亡率": rate
                })

        df = pd.DataFrame(records)

        cause = st.selectbox('死因を選択してください',
                        df["死因"].unique())
        df = df[df["死因"]==cause]
        df.drop("死因",axis=1,inplace=True)
        df.set_index("年次",inplace=True)
with tab1:
    if option=="年別にみる":
        table=st.toggle("表を表示")
        if table==True:
            st.dataframe(df,width=800,height=220)
        st.bar_chart(df)
    elif option=="死因別にみる":
        table=st.toggle("表を表示")
        if table==True:
            st.dataframe(df,width=800,height=220)
        st.line_chart(df)

with tab2:
    if option=="死因別にみる":
        max_rate = df["死亡率"].max()
        min_rate = df["死亡率"].min()
        mean_rate = df["死亡率"].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("最大死亡率", f"{max_rate:.2f}")
        col2.metric("最小死亡率", f"{min_rate:.2f}")
        col3.metric("平均死亡率", f"{mean_rate:.2f}")
    
    if option=="年別にみる":
        max_rate = df["死亡率"].max()
        max_cause = df[df["死亡率"] == max_rate]
        min_rate = df["死亡率"].min()
        min_cause = df[df["死亡率"] == min_rate]

        col1, col2, = st.columns(2)

        col1.subheader("最大死亡率")
        col1.metric(f"死因:{max_cause.index[0]}", f"{max_rate:.2f}")

        col2.subheader("最小死亡率")
        col2.metric(f"死因:{min_cause.index[0]}", f"{min_rate:.2f}")