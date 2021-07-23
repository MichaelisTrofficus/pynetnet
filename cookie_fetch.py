import requests
from helpers.screener import get_filter_data, get_crumb_and_cookie

url_cookie = 'https://finance.yahoo.com/screener/new/'
header, crumb, cookie = get_crumb_and_cookie(url_cookie)
data = get_filter_data()

with requests.session():
    website = requests.post(f"https://query2.finance.yahoo.com/v1/finance/screener?crumb={crumb}&lang=en-US&region=US"
                            f"&formatted=true&corsDomain=finance.yahoo.com", headers=header, cookies=cookie, data=data)
    print(website.content)
