import requests
from datetime import datetime

class TWStockAPI:
    BASE_URL = "https://openapi.twse.com.tw/v1"

    @staticmethod
    def get_stock_info(stock_code):
        url = f"{TWStockAPI.BASE_URL}/exchangeReport/STOCK_DAY_AVG?stockNo={stock_code}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return f"無法獲取股票 {stock_code} 的數據"

            latest_data = data[0]
            stock_name = TWStockAPI.get_stock_name(stock_code)
            
            return {
                "股票代碼": stock_code,
                "股票名稱": stock_name if stock_name else "未知",
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
        except requests.RequestException as e:
            return f"獲取股票 {stock_code} 信息時發生網絡錯誤：{str(e)}"
        except Exception as e:
            return f"獲取股票 {stock_code} 信息時發生錯誤：{str(e)}"

    @staticmethod
    def get_stock_name(stock_code):
        url = f"{TWStockAPI.BASE_URL}/opendata/t187ap03_L"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for stock in data:
                if stock["公司代號"] == stock_code:
                    return stock["公司簡稱"]
        except Exception:
            pass
        return None

# 使用示例
if __name__ == "__main__":
    stock_code = "2330"  # 以台積電為例
    stock_info = TWStockAPI.get_stock_info(stock_code)
    print(stock_info)