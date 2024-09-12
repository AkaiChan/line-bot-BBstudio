import requests
from datetime import datetime
import logging
import json

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
            response.raise_for_status()

            logger.debug(f"API 響應狀態碼: {response.status_code}")
            logger.debug(f"API 響應內容: {response.text[:500]}")  # 輸出前500個字符的響應內容

            # 檢查響應內容是否為空
            if not response.text.strip():
                logger.warning("API 返回空響應")
                return {"error": "API 返回空響應"}

            # 嘗試解析 JSON
            try:
                data = json.loads(response.text)
            except json.JSONDecodeError as json_error:
                logger.error(f"JSON 解析錯誤: {str(json_error)}")
                return {"error": f"JSON 解析錯誤: {str(json_error)}，API 響應: {response.text[:100]}..."}

            if not data:
                return {"error": f"無法獲取股票 {stock_code} 的數據"}

            latest_data = data[0]
            stock_name = TWStockAPI.get_stock_name(stock_code)
            
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
                "漲跌價差": latest_data.get("Change", "N/A"),
                "成交筆數": latest_data.get("Transaction", "N/A")
            }
            logger.debug(f"成功獲取股票 {stock_code} 的信息: {result}")
            return result
        except requests.RequestException as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生網絡錯誤")
            return {"error": f"獲取股票 {stock_code} 信息時發生網絡錯誤：{str(e)}"}
        except Exception as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生未知錯誤")
            return {"error": f"獲取股票 {stock_code} 信息時發生未知錯誤：{str(e)}"}

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
    stock_code = "0050"
    stock_info = TWStockAPI.get_stock_info(stock_code)
    print(stock_info)