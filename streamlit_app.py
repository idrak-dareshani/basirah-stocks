import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/analyze"  # Update if deployed

st.set_page_config(page_title="Shariah Stock Analyzer", layout="wide")

st.title("📈 Shariah-Compliant Stock Analyzer")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, TSLA):")

if ticker:
    with st.spinner("Fetching analysis..."):
        try:
            response = requests.post(API_URL, params={"ticker": ticker})
            if response.status_code != 200:
                st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
            else:
                result = response.json()

                # --- Company Info ---
                st.subheader("🏢 Company Info")
                company = result["company"]
                st.write(f"**Name:** {company['name']}")
                st.write(f"**Sector:** {company['sector']}")
                st.write(f"**Industry:** {company['industry']}")
                st.write(f"**Market Cap:** {company['marketCap']:,}")
                st.write(f"**Summary:** {company['summary']}")

                # --- Financials ---
                st.subheader("💰 Financials")
                st.json(result["financials"])

                # --- Shariah Screening ---
                st.subheader("🕌 Shariah Screening")
                st.json(result["shariah_screening"])

                compliant = result["shariah_screening"]["Shariah Compliant"]
                if compliant:
                    st.success("✅ This company is Shariah-compliant.")
                else:
                    st.warning("⚠️ This company may not be Shariah-compliant.")

                # --- Price Chart ---
                st.subheader("📊 Price Trend (6 months)")
                prices = pd.DataFrame(result["prices"])
                st.line_chart(prices.set_index("Date")["Close"])

                # --- Recommendation ---
                st.subheader("📌 Recommendation")
                st.info(f"**Suggested Action:** {result['recommendation']}")

        except Exception as e:
            st.error(f"Error: {e}")
