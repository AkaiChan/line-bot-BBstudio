import requests
from datetime import date
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TWStockAPI:
    BASE_URL = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY"

    @staticmethod
    def get_stock_info(stock_code):
        logger.debug(f"開始獲取股票 {stock_code} 的信息")
        today = date.today()
        url = f"{TWStockAPI.BASE_URL}?date={today.strftime('%Y%m%d')}&stockNo={stock_code}&response=json"
        try:
            logger.debug(f"正在請求 URL: {url}")
            response = requests.get(url)
            response.raise_for_status()

            logger.debug(f"API 響應狀態碼: {response.status_code}")
            logger.debug(f"API 響應內容: {response.text}")  # 輸出完整的響應內容

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

            if data['stat'] != 'OK':
                logger.warning(f"獲取股票 {stock_code} 信息失敗：{data['stat']}")
                return {"error": f"獲取股票 {stock_code} 信息失敗：{data['stat']}"}

            if not data['data']:
                logger.warning(f"股票 {stock_code} 沒有可用數據")
                return {"error": f"股票 {stock_code} 沒有可用數據"}

            latest_data = data['data'][-1]  # 獲取最新的一天數據
            
            result = {
                "股票代碼": stock_code,
                "日期": latest_data[0],
                "成交股數": latest_data[1],
                "成交金額": latest_data[2],
                "開盤價": latest_data[3],
                "最高價": latest_data[4],
                "最低價": latest_data[5],
                "收盤價": latest_data[6],
                "漲跌價差": latest_data[7],
                "成交筆數": latest_data[8]
            }
            logger.debug(f"成功獲取股票 {stock_code} 的信息: {result}")
            return result
        except requests.RequestException as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生網絡錯誤")
            return {"error": f"獲取股票 {stock_code} 信息時發生網絡錯誤：{str(e)}"}
        except Exception as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生未知錯誤")
            return {"error": f"獲取股票 {stock_code} 信息時發生未知錯誤：{str(e)}"}

# 使用示例
if __name__ == "__main__":
    stock_code = "0050"
    stock_info = TWStockAPI.get_stock_info(stock_code)
    print(stock_info)