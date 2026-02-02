import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title="Stock Quality Screener", layout="wide")

st.title("Smart Stock Quality Screener")
st.caption("Use ALL key financial parameters to filter real quality growth stocks")


uploaded_file = st.file_uploader("Upload your csv file", type=["csv"])

if uploaded_file is not None:

   
    df = pd.read_csv(uploaded_file)

    
    df.columns = df.columns.str.strip().str.replace(r"\s+", " ", regex=True)

  
    numeric_cols = [
        "CMP Rs.", "P/E", "Mar Cap Rs.Cr.", "Div Yld %",
        "NP Qtr Rs.Cr.", "Qtr Profit Var %",
        "Sales Qtr Rs.Cr.", "Qtr Sales Var %", "ROCE %"
    ]

    col_map = {
        "CMP  Rs.": "CMP Rs.",
        "Mar Cap  Rs.Cr.": "Mar Cap Rs.Cr.",
        "Div Yld  %": "Div Yld %",
        "NP Qtr  Rs.Cr.": "NP Qtr Rs.Cr.",
        "Qtr Profit Var  %": "Qtr Profit Var %",
        "Sales Qtr  Rs.Cr.": "Sales Qtr Rs.Cr.",
        "Qtr Sales Var  %": "Qtr Sales Var %",
        "ROCE  %": "ROCE %"
    }

    df.rename(columns=col_map, inplace=True)

    for col in numeric_cols:
        df[col] = (
            df[col].astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=[
        "P/E", "ROCE %", "Mar Cap Rs.Cr.",
        "Qtr Sales Var %", "Qtr Profit Var %",
        "Sales Qtr Rs.Cr.", "NP Qtr Rs.Cr."
    ])

  
    st.sidebar.header("Advanced Filter Settings")

    roce_min = st.sidebar.slider("Minimum ROCE %", 0, 100, 20)
    pe_max = st.sidebar.slider("Maximum P/E", 1, 100, 40)
    mcap_min = st.sidebar.slider("Minimum Market Cap (Cr)", 0, 10000, 500)

    sales_growth_min = st.sidebar.slider("Minimum Qtr Sales Growth %", 0, 200, 10)
    profit_growth_min = st.sidebar.slider("Minimum Qtr Profit Growth %", 0, 200, 10)

    sales_min = st.sidebar.slider("Minimum Qtr Sales (Cr)", 0, 5000, 50)
    profit_min = st.sidebar.slider("Minimum Qtr Profit (Cr)", 0, 1000, 10)

    div_min = st.sidebar.slider("Minimum Dividend Yield %", 0.0, 15.0, 0.0)

  
    filtered = df[
        (df["ROCE %"] > roce_min) &
        (df["P/E"] < pe_max) &
        (df["Mar Cap Rs.Cr."] > mcap_min) &
        (df["Qtr Sales Var %"] > sales_growth_min) &
        (df["Qtr Profit Var %"] > profit_growth_min) &
        (df["Sales Qtr Rs.Cr."] > sales_min) &
        (df["NP Qtr Rs.Cr."] > profit_min) &
        (df["Div Yld %"] >= div_min)
    ].sort_values(by="ROCE %", ascending=False)

    top_15 = filtered.head(15)

   
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Stocks Found", len(filtered))
    c2.metric("Best ROCE", f"{top_15['ROCE %'].max():.2f} %")
    c3.metric("Average P/E", f"{top_15['P/E'].mean():.2f}")
    c4.metric("Average Market Cap", f"{top_15['Mar Cap Rs.Cr.'].mean():.0f} Cr")

    st.divider()

    st.subheader("Top 15 Quality Stocks")

    show_cols = [
        "Name", "CMP Rs.", "P/E", "ROCE %",
        "Mar Cap Rs.Cr.", "Sales Qtr Rs.Cr.",
        "Qtr Sales Var %", "NP Qtr Rs.Cr.",
        "Qtr Profit Var %", "Div Yld %"
    ]

    st.dataframe(
        top_15[show_cols].style.background_gradient(cmap="Greens"),
        use_container_width=True
    )

  
    st.subheader(" ROCE Comparison")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_15["Name"], top_15["ROCE %"])
    ax.invert_yaxis()
    ax.set_xlabel("ROCE %")
    st.pyplot(fig)

    
    csv = top_15[show_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Filtered Stocks CSV",
        data=csv,
        file_name="Top_Quality_Stocks.csv",
        mime="text/csv"
    )

else:
    st.info("Upload your CSV file to start the screener.")
