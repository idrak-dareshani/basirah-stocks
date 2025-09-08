# Sharia Stock Analyst — MVP

This repository contains a minimal, runnable MVP for a Sharia-compliant stock analysis system.
It includes a FastAPI backend that fetches price and fundamentals data (via yfinance / Financial Modeling Prep),
performs Sharia screening and technical/fundamental scoring, and returns a decision.

A simple Streamlit frontend is included to demo the API locally.

## Files
- `api/main.py` - FastAPI app
- `data_fetcher.py` - price & fundamentals fetchers (yfinance + FMP wrapper)
- `sharia_screen.py` - business & financial screening rules
- `technicals.py` - technical indicators & trend scoring (pandas-ta)
- `fundamentals.py` - fundamentals scoring helper
- `decision_engine.py` - combine scores into a recommendation
- `streamlit_app.py` - simple frontend to call the API and display results
- `requirements.txt` - Python dependencies
- `README.md` - this file

## Quick start (local)
1. Clone or download the repo.
2. Create a virtualenv and install requirements:
   ```bash
   python -m venv .venv
   source .venv/bin/activate     # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Fill `.env` values (see `.env.example`) if you want to use Financial Modeling Prep (FMP).
4. Run backend:
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```
5. In another terminal, run the Streamlit frontend:
   ```bash
   streamlit run streamlit_app.py
   ```
6. Open http://localhost:8501

## Notes
- This is a minimal MVP for research & prototyping. Do not use for live trading.
- For authoritative Sharia screening, integrate a paid provider (Zoya, IdealRatings) or consult scholars.
