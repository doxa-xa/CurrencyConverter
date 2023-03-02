import requests
import json
from converter.currencies import Currency
from converter.config import api_key

class Connect:

    @staticmethod
    def get_rates(base):
        symbols = ''
        
        currency_list = [i.name for i in Currency]

        for i in currency_list:
            symbols = symbols + ','+ i  

        symbols = symbols[1:]
        # print(symbols)

        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"
        payload = {}
        headers= {
        "apikey": api_key
        }
        response = requests.request("GET", url, headers=headers, data = payload)
        status_code = response.status_code
        result = json.loads(response.text)

        return result["rates"]
    