from __future__ import annotations

from typing import List
import requests
import re
import json

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

    def get_data(self) -> List[dict]:
        """
        Gets all the data fitting the provided filters.
        :return: A list of dictionaries containing all the information needed for posterior fundamental analysis
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
            data = json.loads(response.content).get('finance').get('result')[0]
            if body['offset'] > data['total']:
                end = True
            body['offset'] += body['size']

            quotes.extend(data['quotes'])
        return quotes
