from __future__ import annotations

from typing import List
from yfinance.ticker import Ticker
import yfinance as yf
from pynetnet.YahooScreener import YahooScreener
from tqdm import tqdm
import json


class NetNetScreener:

    def __init__(self, data: List[dict]):
        self.data = data
        self.tickers = []
        self.error_tickers = []

        print(f"Initial number of candidate stocks: {len(data)}")
        self._prefilter()
        print(f"Number of stocks after prefiltering: {len(self.tickers)}")

    def _prefilter(self):
        """
        Filters those stocks with market to value less than 1 (inverse of the P / B)
        or those which have no P/B data. It also retrieves its tickers.
        """
        tickers = []
        for stock in tqdm(self.data):
            symbol = stock.get("symbol")
            try:
                if (1 / stock["priceToBook"]["raw"]) > 1:
                    tickers.append(symbol)
            except KeyError:
                self.error_tickers.append(symbol)
        self.tickers = tickers

    @staticmethod
    def is_net_net(ticker: str) -> bool:
        """
        Applies filter from the book to check if it's a net-net
        :param ticker: Ticker
        :return: boolean
        """

        ticker_data = yf.Ticker(ticker)

        # TODO: Create an internal object that wraps this behaviour
        info = ticker_data.info
        balance_sheet = ticker_data.balance_sheet
        # quarterly_balance_sheet = ticker_data.quarterly_balance_sheet
        # quarterly_cash_flow = ticker_data.quarterly_cashflow

        # selling_shares = quarterly_cash_flow.loc["Total Cashflows From Investing Activities"]

        market_cap = info.get("marketCap")
        sector = info.get("sector")
        country = info.get("country")
        debt_to_equity = info.get("debtToEquity")
        current_ratio = info.get("currentRatio")

        # Objective 1

        # Filter 1: Low Average Daily Volume
        # This depends on the investor's capital
        # TODO: Introduce this in the future

        # Filter 2: Market Capitalisation above 100M and below 1M.
        if market_cap < 1000000 or market_cap > 100000000:
            return False

        # Filter 3: Prohibited industries
        if sector == "Financial Services":
            return False

        # Filter 4: No NYSE
        # TODO: Check where to find this information

        # Filter 5: Major Chinese business operations
        if country == "China":
            return False

        # Objective 2

        # Filter 6: Positive NCAV
        last_balance_sheet = balance_sheet.iloc[:, 0].to_dict()  # Last Annual balance sheet

        current_assets = last_balance_sheet.get("Total Current Assets")
        total_liabilities = last_balance_sheet.get("Total Liab")
        preliminary_ncav = current_assets - total_liabilities

        if preliminary_ncav < 0:
            return False

        # Filter 7: Market Capitalisation less than preliminary NCAV
        if preliminary_ncav < market_cap:
            return False

        # Filter 8: Debt to Equity Ratio below 50%
        if debt_to_equity > 50:
            return False

        # Filter 9: Current Ratio Assessment
        if current_ratio < 1.5:
            return False

        # Filter 10: Not selling Shares
        # if any(selling_shares > 0):
        #    return False

        # Filter 11: Reasonable Burn Rate
        # TODO: Year over year and quarter over quarter

        return True

    def find_net_nets(self) -> List[str]:
        """
        Finds the possible net nets among the prefiltered stocks
        :return: a list of Ticker objets containing information of each candidate net-net
        """

        net_nets = []
        for ticker in tqdm(self.tickers):
            if self.is_net_net(ticker):
                net_nets.append(ticker)

        return net_nets


if __name__ == "__main__":
    ex = YahooScreener(["us"])
    data = ex.get_data()

    nns = NetNetScreener(data)
    net_nets = nns.find_net_nets()
    print(net_nets)
