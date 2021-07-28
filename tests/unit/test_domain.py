import pytest
from pynetnet.domain.model import Company, InvalidCompanyError, NetNetFilter


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


@pytest.fixture
def one_net_net():
    # First company is a net-net. Second one is a Chinese company (not a net-net)
    fundamentals = [{"name": "Example", "ticker": "EXMPL", "country": "United States",
                     "sector": "Retail", "market_cap": 50000000, "price_to_book": 0.56,
                     "current_assets": 10000000000000, "total_liabilities": 2000,
                     "current_ratio": 3.56, "debt_to_equity": 20},
                    {"name": "Example", "ticker": "EXMPL", "country": "China",
                     "sector": "Retail", "market_cap": 50000000, "price_to_book": 0.56,
                     "current_assets": 10000, "total_liabilities": 2000,
                     "current_ratio": 2.5, "debt_to_equity": 20}]

    companies = [Company(fundamentals[0]), Company(fundamentals[1])]
    return companies


def test_invalid_company(invalid_fundamentals):
    with pytest.raises(InvalidCompanyError):
        Company(invalid_fundamentals)


def test_preliminary_ncav(valid_fundamentals):
    company = Company(valid_fundamentals)
    assert company.get_preliminary_ncav() == 8000


def test_find_net_net(one_net_net):
    nnf = NetNetFilter()
    assert nnf.filter_net_nets(one_net_net)[0] == one_net_net[0]
