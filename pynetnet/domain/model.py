from __future__ import annotations

from typing import List


class Company:
    """
    Entity representing a Company with one attribute, 'fundamentals' which contains the parameters
    needed to assess if it's a net-net.

     Attributes
     ----------
     name: str
     ticker: str
     country: str
     sector: str
     market_cap: float
     price_to_book: float
     current_assets: float
     total_liabilities: float
     current_ratio: float
     debt_to_equity: float

     Methods
     -------
     __init__(fundamentals: dict):
        Object creation. The parameter "fundamentals" contains data needed to assess if company is a net-net. For
        example:

            {
                "name": "Example", "ticker": "EXMPL", "country": "United States",
                "sector": "Retail", "market_cap": 100000000, "price_to_book": 0.56,
                "current_assets": 10000, "total_liabilities": 2000,
                "current_ratio": 2.5, "debt_to_equity": 40
            }

     _check():
        Checks if the data contained in the fundamentals is valid. If just one of the variables is not informed
        then the class will raise an InvalidCompanyError.

     _generate_attributes(fundamentals: dict):
        Generates all attributes from "fundamentals" dictionary
     """

    def __init__(self, fundamentals: dict):
        self._check(fundamentals)
        self._generate_attributes(fundamentals)

    def __eq__(self, other):
        if not isinstance(other, Company):
            return False
        return other.ticker == self.ticker

    @staticmethod
    def _check(fundamentals: dict):
        for value in fundamentals.values():
            if not value:
                raise InvalidCompanyError

    def _generate_attributes(self, fundamentals: dict):

        # TODO: maybe change with : [setattr(self, key, fundamentals[key]) for key in fundamentals]. Not clear enough?
        self.name = fundamentals.get("name")
        self.ticker = fundamentals.get("ticker")
        self.country = fundamentals.get("country")
        self.sector = fundamentals.get("sector")
        self.market_cap = fundamentals.get("market_cap")
        self.price_to_book = fundamentals.get("price_to_book")
        self.current_assets = fundamentals.get("current_assets")
        self.total_liabilities = fundamentals.get("total_liabilities")
        self.current_ratio = fundamentals.get("current_ratio")
        self.debt_to_equity = fundamentals.get("debt_to_equity")

        # TODO: Then we have to get information abour preferred shares and add this here
        self.preliminary_ncav = self.current_assets - self.total_liabilities

    def get_name(self):
        return self.name

    def get_ticker(self):
        return self.ticker

    def get_country(self):
        return self.country

    def get_sector(self):
        return self.sector

    def get_market_cap(self):
        return self.market_cap

    def get_price_to_book(self):
        return self.price_to_book

    def get_current_assets(self):
        return self.current_assets

    def get_total_liabilities(self):
        return self.total_liabilities

    def get_current_ratio(self):
        return self.current_ratio

    def get_debt_to_equity(self):
        return self.debt_to_equity

    def get_preliminary_ncav(self):
        return self.preliminary_ncav


class InvalidCompanyError(Exception):
    """
    Raise if some of the company's data is missing
    """
    pass


class NetNetFilter:
    """
     Criteria pattern for selecting net-nets.

     Methods
     -------
     filter_net_nets():
        Filter those companies that satisfy the conditions to be considered as net-nets.
     """

    # TODO: We need to add more filters (preferred shares, company selling shares, NYSE, etc.)
    @staticmethod
    def filter_net_nets(companies: List[Company]) -> List[Company]:

        net_nets = []
        for company in companies:

            net_net_rules = [
                (1 / company.get_price_to_book()) > 1,  # Inverse of P/B greater than 1 (exclude negative values)
                company.get_market_cap() > 1000000 or company.get_market_cap() < 100000000,
                company.get_sector() != "Financial Services",
                company.get_country() != "China",
                company.get_preliminary_ncav() > 0,
                company.get_preliminary_ncav() > company.get_market_cap(),
                company.get_debt_to_equity() < 50,
                company.get_current_ratio() > 1.5
            ]

            if all(net_net_rules):
                net_nets.append(company)

        return net_nets
