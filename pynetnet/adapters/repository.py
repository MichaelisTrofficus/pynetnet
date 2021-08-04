from __future__ import annotations

from typing import List
import logging
from tqdm import tqdm
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from pynetnet.adapters.yahoo import YahooScreener, YahooAPI
from pynetnet.domain.model import Company, InvalidCompanyError

MAX_NUM_WORKERS = multiprocessing.cpu_count()


class YahooRepository:
    def __init__(self, countries: List[str]):
        self.countries = countries

    def get(self) -> List[Company]:

        # Instantiate Yahoo classes
        yahoo_screener = YahooScreener(self.countries)
        yahoo_api = YahooAPI()

        # We fetch tickers
        tickers = yahoo_screener.get_data()

        # We fetch fundamental information about the tickers
        # and generate company entities
        companies = []

        for ticker in tqdm(tickers):
            try:
                fundamentals = yahoo_api.get_data(ticker)
                company = Company(fundamentals)
                companies.append(company)
            except InvalidCompanyError:
                logging.warning(f"Company with ticker {ticker} with invalid data")
            except Exception as e:
                logging.warning(f"Unknown error with ticker {ticker}")

        return companies


if __name__ == "__main__":
    yahoo_repository = YahooRepository(["us"])
    companies = yahoo_repository.get()
    print(1)

