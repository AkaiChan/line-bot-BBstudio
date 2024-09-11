import requests

def get_stock_info(stock_code):
    base_url = "https://openapi.twse.com.tw/v1"
    endpoint = f"/exchangeReport/STOCK_DAY_AVG?stockNo={stock_code}"
    
    try:
        response = requests.get(base_url + endpoint)
        response.raise_for_status()  # 如果狀態碼不是 200，會拋出異常
        stock_data = response.json()
        
        if stock_data:
            latest_data = stock_data[0]  # 獲取最新的數據
            stock_info = (
                f"股票代碼 {stock_code} 的資訊：\n"
                f"日期：{latest_data['date']}\n"
                f"成交股數：{latest_data['volumeOfTransactions']} 股\n"
                f"成交金額：{latest_data['valueOfTransactions']} 元\n"
                f"開盤價：{latest_data['openingPrice']} 元\n"
                f"最高價：{latest_data['highestPrice']} 元\n"
                f"最低價：{latest_data['lowestPrice']} 元\n"
                f"收盤價：{latest_data['closingPrice']} 元\n"
                f"漲跌：{latest_data['change']} 元\n"
                f"成交筆數：{latest_data['numberOfTransactions']} 筆"
            )
            return stock_info
        else:
            return f"無法獲取股票代碼 {stock_code} 的資訊。"

    except requests.exceptions.RequestException as e:
        return f"獲取股票資訊時發生錯誤：{str(e)}"
