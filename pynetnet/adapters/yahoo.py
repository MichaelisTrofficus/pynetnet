from __future__ import annotations

from typing import List
import requests
import yfinance as yf
import re
import json
import logging

COMMON_HEADER = {'Connection': 'keep-alive',
                 'Expires': '-1',
                 'Upgrade-Insecure-Requests': '1',
                 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
                 }


class YahooScreener:
    """
     This class emulates the Yahoo Screener with the following filter params:

        1. Small caps (in this case less than 100M)
        2. Price to Book less than 1 (it's an initial estimate of an undervalued company)
        3. Country -> we provide a selector for the user to choose a set of countries

     Attributes
     ----------
     countries : List[str]
         A list of countries
     crumb : str
         Crumb needed to fetch the data from Yahoo Screener
     cookies : CookieJar
         Cookies needed to fetch the data from Yahoo Screener

     Methods
     -------
     _prepare():
        Gets the crumb and the cookies from the website.

     get_data():
        Gets all the data fitting the provided filters.
     """

    def __init__(self, countries: List[str]):
        self.countries = countries
        self._prepare()

    def _prepare(self):
        website = requests.get(
            "https://finance.yahoo.com/screener/new/", headers=COMMON_HEADER)
        self.crumb = re.findall(
            '"CrumbStore":{"crumb":"(.+?)"}', str(website.content))[0]
        self.cookies = website.cookies

    def get_data(self) -> List[str]:
        """
        Gets all the tickers fitting the provided filters.
        :return: A list of tickers for the candidates net-nets
        """

        countries_filter = [{"operator": "EQ", "operands": ["region", c]} for c in self.countries]

        body = {
            "size": 200,
            "offset": 0,
            "sortField": "intradaymarketcap",
            "sortType": "DESC",
            "quoteType": "EQUITY",
            "topOperator": "AND",
            "query": {
                "operator": "AND",
                "operands": [
                    {
                        "operator": "or",
                        "operands": countries_filter
                    },
                    # Small caps -> Less than 100M according to Net-Net Investing Philosophy
                    {
                        "operator": "or",
                        "operands": [
                            {
                                "operator": "LT",
                                "operands": [
                                    "intradaymarketcap",
                                    100000000
                                ]
                            }
                        ]
                    },
                    # P/B less than 1 -> This is some initial approximation
                    {
                        "operator": "lt",
                        "operands": [
                            "lastclosepricebookvalue.lasttwelvemonths",
                            1
                        ]
                    }
                ]
            }
        }

        quotes = []
        end = False

        while not end:

            response = requests.post(
                f"https://query2.finance.yahoo.com/v1/finance/screener?crumb={self.crumb}&lang=en-US&region=US"
                f"&formatted=true&corsDomain=finance.yahoo.com", cookies=self.cookies, data=json.dumps(body),
                headers=COMMON_HEADER)

            try:
                data = json.loads(response.content).get('finance').get('result')[0]
            except json.decoder.JSONDecodeError:
                logging.error("Data not received from Yahoo Finance. Please, try again later")
                return []
            except TypeError:
                logging.error("Data not received from Yahoo Finance. Plase, try again later")
                return []

            if body['offset'] > data['total']:
                end = True

            body['offset'] += body['size']
            quotes.extend(data['quotes'])

        tickers = [c.get("symbol") for c in quotes]

        return tickers


class YahooAPI:

    def get_data(self, ticker: str) -> dict:
        # Fetch ticker's data
        ticker_data = yf.Ticker(ticker)

        info = ticker_data.info  # Company's Summary
        balance_sheet = ticker_data.balance_sheet  # Company's Balance Sheet
        last_balance_sheet = balance_sheet.iloc[:, 0].to_dict()  # Last Annual balance sheet
        # quarterly_balance_sheet = ticker_data.quarterly_balance_sheet
        # quarterly_cash_flow = ticker_data.quarterly_cashflow

        return {
            "name": info.get("longName"),
            "ticker": ticker,
            "country": info.get("country"),
            "sector": info.get("sector"),
            "market_cap": info.get("marketCap"),
            "price_to_book": info.get("priceToBook"),
            "current_assets": last_balance_sheet.get("Total Current Assets"),
            "total_liabilities":  last_balance_sheet.get("Total Liab"),
            "current_ratio": info.get("currentRatio"),
            "debt_to_equity": info.get("debtToEquity")
        }
