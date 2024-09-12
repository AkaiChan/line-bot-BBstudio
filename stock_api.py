import requests
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TWStockAPI:
    BASE_URL = "https://openapi.twse.com.tw/v1"

    @staticmethod
    def get_stock_info(stock_code):
        url = f"{TWStockAPI.BASE_URL}/exchangeReport/STOCK_DAY_AVG?stockNo={stock_code}"
        try:
            logger.debug(f"正在請求 URL: {url}")
            response = requests.get(url)
            response.raise_for_status()  # 如果狀態碼不是 200，將引發異常
            
            logger.debug(f"API 響應內容: {response.text}")
            data = response.json()
            
            if not data:
                return f"無法獲取股票 {stock_code} 的數據，API 返回空結果"

            latest_data = data[0]
            stock_name = TWStockAPI.get_stock_name(stock_code)
            
            return (
                f"股票代碼：{stock_code}\n"
                f"股票名稱：{stock_name if stock_name else '未知'}\n"
                f"日期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"成交股數：{latest_data['TradeVolume']}\n"
                f"成交金額：{latest_data['TradeValue']}\n"
                f"開盤價：{latest_data['OpeningPrice']}\n"
                f"最高價：{latest_data['HighestPrice']}\n"
                f"最低價：{latest_data['LowestPrice']}\n"
                f"收盤價：{latest_data['ClosingPrice']}\n"
                f"漲跌：{latest_data['Change']}\n"
                f"成交筆數：{latest_data['Transaction']}"
            )
        except requests.RequestException as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生網絡錯誤")
            return f"獲取股票 {stock_code} 信息時發生網絡錯誤：{str(e)}"
        except json.JSONDecodeError as e:
            logger.exception(f"解析股票 {stock_code} 數據時發生錯誤")
            return f"解析股票 {stock_code} 數據時發生錯誤：{str(e)}"
        except Exception as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生未知錯誤")
            return f"獲取股票 {stock_code} 信息時發生未知錯誤：{str(e)}"

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
        except Exception as e:
            logger.exception(f"獲取股票 {stock_code} 名稱時發生錯誤")
        return None

# 使用示例
if __name__ == "__main__":
    stock_code = "0050"
    stock_info = TWStockAPI.get_stock_info(stock_code)
    print(stock_info)