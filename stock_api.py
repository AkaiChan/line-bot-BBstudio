import requests
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TWStockAPI:
    BASE_URL = "https://openapi.twse.com.tw/v1"

    @staticmethod
    def get_stock_info(stock_code):
        logger.debug(f"開始獲取股票 {stock_code} 的信息")
        try:
            # 獲取當日個股資訊
            url = f"{TWStockAPI.BASE_URL}/exchangeReport/STOCK_DAY_AVG?stockNo={stock_code}"
            response = requests.get(url)
            response.raise_for_status()
            daily_data = response.json()

            if not daily_data:
                return {"error": f"無法獲取股票 {stock_code} 的數據"}

            latest_data = daily_data[0]

            # 獲取股票名稱
            stock_name = TWStockAPI.get_stock_name(stock_code)

            # 獲取昨日收盤價
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
            url_yesterday = f"{TWStockAPI.BASE_URL}/exchangeReport/STOCK_DAY_AVG?date={yesterday}&stockNo={stock_code}"
            response_yesterday = requests.get(url_yesterday)
            response_yesterday.raise_for_status()
            yesterday_data = response_yesterday.json()
            yesterday_close = yesterday_data[0]['ClosingPrice'] if yesterday_data else 'N/A'

            result = {
                "股票代碼": stock_code,
                "股票名稱": stock_name if stock_name else "未知",
                "日期": latest_data.get("Date", datetime.now().strftime("%Y-%m-%d")),
                "成交股數": latest_data.get("TradeVolume", "N/A"),
                "成交金額": latest_data.get("TradeValue", "N/A"),
                "開盤價": latest_data.get("OpeningPrice", "N/A"),
                "最高價": latest_data.get("HighestPrice", "N/A"),
                "最低價": latest_data.get("LowestPrice", "N/A"),
                "收盤價": latest_data.get("ClosingPrice", "N/A"),
                "漲跌": latest_data.get("Change", "N/A"),
                "昨日收盤價": yesterday_close,
                "漲跌幅": f"{float(latest_data.get('Change', 0)) / float(yesterday_close) * 100:.2f}%" if yesterday_close != 'N/A' else 'N/A'
            }
            logger.debug(f"成功獲取股票 {stock_code} 的信息: {result}")
            return result
        except requests.RequestException as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生網絡錯誤")
            return {"error": f"獲取股票 {stock_code} 信息時發生網絡錯誤：{str(e)}"}
        except Exception as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生錯誤")
            return {"error": f"獲取股票 {stock_code} 信息時發生錯誤：{str(e)}"}

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
            logger.exception(f"獲取股票 {stock_code} 名稱時發生錯誤")
        return None

# 使用示例
if __name__ == "__main__":
    stock_code = "2330"  # 以台積電為例
    stock_info = TWStockAPI.get_stock_info(stock_code)
    print(stock_info)