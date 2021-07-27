import pytest
from pynetnet.domain.model import Company, InvalidCompanyError


@pytest.fixture
def valid_fundamentals():
    return {"name": "Example", "ticker": "EXMPL", "country": "United States",
            "sector": "Retail", "market_cap": 100000000, "price_to_book": 0.56,
            "current_assets": 10000, "total_liabilities": 2000,
            "current_ratio": 2.5, "debt_to_equity": 40}


@pytest.fixture
def invalid_fundamentals():
    return {"name": "Example", "ticker": "EXMPL", "country": "United States",
            "sector": "Retail", "market_cap": None, "price_to_book": 0.56,
            "current_assets": 10000, "total_liabilities": 2000,
            "current_ratio": 2.5, "debt_to_equity": None}


def test_invalid_company(invalid_fundamentals):
    with pytest.raises(InvalidCompanyError):
        _ = Company(invalid_fundamentals)


def test_preliminary_ncav(valid_fundamentals):
    company = Company(valid_fundamentals)
    assert company.get_preliminary_ncav() == 8000
