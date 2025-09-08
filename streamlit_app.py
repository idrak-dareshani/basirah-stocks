import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_BASE = st.sidebar.text_input("API base URL", "http://localhost:8000")

st.title("Sharia Stock Analyst — MVP")
ticker = st.text_input("Ticker (e.g. AAPL)", "AAPL")
if st.button("Analyze"):
    with st.spinner("Calling backend..."):
        r = requests.get(f"{API_BASE}/analyze", params={"ticker": ticker})
        if r.status_code != 200:
            st.error(r.text)
        else:
            data = r.json()
            st.subheader("Decision")
            st.json(data["decision"])
            st.subheader("Sharia Screening")
            st.json(data["sharia_business"])
            st.subheader("Financial Ratios")
            st.json(data["financial_ratios"])
            st.subheader("Technical Snapshot")
            tech = data.get("technical", {}).get("latest", {})
            if tech:
                df = pd.DataFrame([tech])
                st.write(df.T)
            st.write("\n\n---\nDisclaimer: This tool is a prototype for research and not investment advice.")
