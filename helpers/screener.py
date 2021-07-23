# Some useful functions to fetch the information from Yahoo Finace Screener
import json
from random import randint
from typing import Tuple
from bs4 import BeautifulSoup
import requests
import re
from requests.cookies import RequestsCookieJar


def get_random_user_agent() -> str:
    """
    Generates a random User Agent
    :return: A string that contains a valid User Agent
    """

    user_agents = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 "
                   "Safari/537.36",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) "
                   "Version/9.0.2 Safari/601.3.9",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 "
                   "Safari/537.36",
                   "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR "
                   "3.0.4506.2152; .NET CLR 3.5.30729)",
                   "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 "
                   "Safari/537.36",
                   "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"]
    return user_agents[randint(0, len(user_agents) - 1)]


def get_crumb_and_cookie(url: str) -> Tuple[dict, str, RequestsCookieJar]:
    """
    This method fetchs a crumb and a cookie from the url provided
    :return:
    """

    header = {'Connection': 'keep-alive',
              'Expires': '-1',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': get_random_user_agent()
              }

    website = requests.get(url, headers=header)
    soup = BeautifulSoup(website.text, 'lxml')
    crumb = str(re.findall('"CrumbStore":{"crumb":"(.+?)"}', str(soup))[0])
    cookies = website.cookies

    return header, crumb, cookies


# TODO: HAY QUE METER AQUI EL PAGINADOOOO
def get_filter_data() -> str:
    """
    For now, it will just create a query for stocks belonging to UK and US, with small cap and a P/B value less than
    # TODO: Of course this functionality has to be extended! Some ideas:
    # TODO: 1. The user may choose the stock's cap by hand (less than 10M, less than 80B, etc.)
    # TODO: 2. The user may filter by others valuation metrics (P/E)
    # TODO: 3. The set of countries available must be extended
    :return:
    """
    data = {
        "size": 200,
        "offset": 1,
        "sortField": "intradaymarketcap",
        "sortType": "DESC",
        "quoteType": "EQUITY",
        "topOperator": "AND",
        "query": {
            "operator": "AND",
            "operands": [
                {
                    "operator": "or",
                    "operands": [
                        {
                            "operator": "EQ",
                            "operands": [
                                "region",
                                "us"
                            ]
                        }
                    ]
                },
                {
                    "operator": "or",
                    "operands": [
                        {
                            "operator": "LT",
                            "operands": [
                                "intradaymarketcap",
                                2000000000
                            ]
                        }
                    ]
                }
            ]
        },
        "userId": "F33IB2UDLZKB6JGIBIVDAT3BTU",
        "userIdType": "guid"
    }

    return json.dumps(data)




