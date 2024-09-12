import requests
from datetime import datetime, date
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TWStockAPI:
    BASE_URL = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY"

    @staticmethod
    def get_stock_info(stock_code):
        today = date.today()
        url = f"{TWStockAPI.BASE_URL}?date={today.strftime('%Y%m%d')}&stockNo={stock_code}&response=json"
        try:
            logger.debug(f"正在請求 URL: {url}")
            response = requests.get(url)
            response.raise_for_status()

            logger.debug(f"API 響應狀態碼: {response.status_code}")
            logger.debug(f"API 響應內容: {response.text[:200]}...")  # 只顯示前200個字符

            data = response.json()
            
            if data['stat'] != 'OK':
                return f"獲取股票 {stock_code} 信息失敗：{data['stat']}"

            latest_data = data['data'][-1]  # 獲取最新的一天數據
            
            return (
                f"股票代碼：{stock_code}\n"
                f"日期：{latest_data[0]}\n"
                f"成交股數：{latest_data[1]}\n"
                f"成交金額：{latest_data[2]}\n"
                f"開盤價：{latest_data[3]}\n"
                f"最高價：{latest_data[4]}\n"
                f"最低價：{latest_data[5]}\n"
                f"收盤價：{latest_data[6]}\n"
                f"漲跌價差：{latest_data[7]}\n"
                f"成交筆數：{latest_data[8]}"
            )
        except requests.RequestException as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生網絡錯誤")
            return f"獲取股票 {stock_code} 信息時發生網絡錯誤：{str(e)}"
        except Exception as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生未知錯誤")
            return f"獲取股票 {stock_code} 信息時發生未知錯誤：{str(e)}"

# 使用示例
if __name__ == "__main__":
    stock_code = "0050"
    stock_info = TWStockAPI.get_stock_info(stock_code)
    print(stock_info)