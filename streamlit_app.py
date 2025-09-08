import streamlit as st
import requests

st.title("Shariah Stock Analyst")

ticker = st.text_input("Enter Stock Ticker", "AAPL")

if st.button("Analyze"):
    with st.spinner("Fetching and analyzing data..."):
        result = requests.post("http://localhost:8000/analyze", params={"ticker": ticker}).json()

    st.subheader("Sharīʿah Compliance")
    if result["shariah"]["status"]:
        st.success("✅ Compliant")
    else:
        st.error("❌ Non-compliant")
        st.write("Issues found:")
        for issue in result["shariah"]["issues"]:
            st.write(f"- {issue}")

    st.subheader("Recommendation")
    st.info(result["recommendation"])
