import requests
from datetime import datetime

class TWStockAPI:
    BASE_URL = "https://openapi.twse.com.tw/v1"

    @staticmethod
    def get_stock_info(stock_code):
        url = f"{TWStockAPI.BASE_URL}/exchangeReport/STOCK_DAY_AVG?stockNo={stock_code}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                latest_data = data[0]
                return {
                    "股票代碼": stock_code,
                    "日期": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "成交股數": latest_data["TradeVolume"],
                    "成交金額": latest_data["TradeValue"],
                    "開盤價": latest_data["OpeningPrice"],
                    "最高價": latest_data["HighestPrice"],
                    "最低價": latest_data["LowestPrice"],
                    "收盤價": latest_data["ClosingPrice"],
                    "漲跌": latest_data["Change"],
                    "成交筆數": latest_data["Transaction"]
                }
        return None

    @staticmethod
    def get_stock_name(stock_code):
        url = f"{TWStockAPI.BASE_URL}/opendata/t187ap03_L"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for stock in data:
                if stock["公司代號"] == stock_code:
                    return stock["公司簡稱"]
        return None