import pytest
from sharia_screen import business_activity_screen, financial_ratio_screen

def test_business_screen_no_profile():
    res = business_activity_screen({})
    assert isinstance(res, dict)

def test_financial_ratio_screen_default():
    res = financial_ratio_screen({}, avg_market_cap=1_000_000)
    assert isinstance(res, dict)
