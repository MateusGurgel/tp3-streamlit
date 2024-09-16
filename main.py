import streamlit as st
import pandas as pd


if 'bg_color' not in st.session_state:
    st.session_state.bg_color = "#000000"

if 'font_color' not in st.session_state:
    st.session_state.font_color = "#FFFFFF"


st.session_state.bg_color = st.color_picker('Escolha a cor de fundo', st.session_state.bg_color )
st.session_state.font_color = st.color_picker('Escolha a cor da fonte', st.session_state.font_color)


st.markdown(f"""
    <style>
    .stApp {{
        background-color: {st.session_state.bg_color};
        color: {st.session_state.font_color};
    }}
    p {{
        color: {st.session_state.font_color};
    }}
    </style>
    """, unsafe_allow_html=True)


file = st.file_uploader("Realizando Upload", type=["csv"])

if file is not None:
    dataframe = pd.read_csv(file)

    min_year = st.slider("Dados desde: ", 1990, 2024, 1990)

    with st.spinner(text="In progress"):

        dataframe_filtered = dataframe[dataframe["Year"] >= min_year]

        st.write(dataframe_filtered)

        register_count = dataframe_filtered.shape[0]
        daily_rate_mean = dataframe_filtered["Daily rate"].mean()

        st.write(f"Quantidade de registros: {register_count}")
        st.write(f"Diária média: {daily_rate_mean}")

        dataframe_filtered["date"] = pd.to_datetime(dataframe_filtered[["Year", "Month"]].assign(day=1))

        st.line_chart(dataframe_filtered, x="date", x_label="Ano", y="Daily rate", y_label="Diárias")  

        daily_rate_per_month = dataframe_filtered.groupby("Month")["Daily rate"].mean()

        st.bar_chart(dataframe_filtered, x="Month", x_label="Mês", y="Daily rate", y_label="Diárias")  


        st.download_button("Download file", dataframe_filtered.to_csv())


