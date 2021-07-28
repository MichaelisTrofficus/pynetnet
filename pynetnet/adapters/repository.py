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
            fundamentals = yahoo_api.get_data(ticker)
            try:
                company = Company(fundamentals)
                companies.append(company)
            except InvalidCompanyError:
                logging.info(f"Company with ticker {ticker} with invalid data")

        # TODO: Add code for ThreadPoolExecutor.
        # with ThreadPoolExecutor(max_workers=MAX_NUM_WORKERS) as pool:
        #   results = list(tqdm(pool.map(yahoo_api.get_data, range(len(tickers))), total=len(tickers)))

        return companies


if __name__ == "__main__":

    yahoo_repository = YahooRepository(["us"])
    yahoo_repository.get()

