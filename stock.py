from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
from io import StringIO
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yfinance as yf

def main_fun():
    # 假設我們有一個包含公司資訊的列表
    companies = [
        {"name": "公司A", "code": "1234"},
        {"name": "公司B", "code": "5678"},
        # ... 更多公司
    ]

    result = {
        "message": "Nicole~~~~~~~~",
        "data": {
            "buy": [],
            "sell": [],
            "hold": []
        },
        "signature": "此致，\nAkai"
    }

    for company in companies:
        ws_name = f"{company['name']}|{company['code']}"
        str_company_code = company['code']

        z_value, z2_value, pe_ratio = get_new_data(str_company_code)

        z_value = "-" if z_value == 0 else round(z_value, 2)
        z2_value = "-" if z2_value == 0 else round(z2_value, 2)
        pe_ratio = "-" if pe_ratio == 0 else round(pe_ratio, 2)

        # 假設我們有一個函數來確定買賣建議
        recommendation = get_recommendation(z_value, z2_value, pe_ratio)

        row_data = {
            "company": ws_name,
            "recommendation": recommendation,
            "pe_ratio": pe_ratio,
            "z_value": z_value,
            "z2_value": z2_value
        }

        if recommendation == "Buy":
            result["data"]["buy"].append(row_data)
        elif recommendation == "Sell":
            result["data"]["sell"].append(row_data)
        else:
            result["data"]["hold"].append(row_data)

    return json.dumps(result, ensure_ascii=False, indent=2)

def get_new_data(str_code):
    # 獲取歷史價格數據
    url = f"https://www.cnyes.com/twstock/ps_historyprice.aspx?code={str_code}"
    params = {
        'ctl00$ContentPlaceHolder1$startText': (datetime.now() - timedelta(days=3*365+180)).strftime('%Y/%m/%d'),
        'ctl00$ContentPlaceHolder1$endText': datetime.now().strftime('%Y/%m/%d')
    }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    df = None
    for table in tables:
        try:
            df_temp = pd.read_html(str(table))[0]
            if '日期' in df_temp.columns:
                df = df_temp
                break
        except:
            continue
    
    if df is None:
        print("無法找到歷史價格數據表格")
        return 0, 0, 0

    pe_ratio = get_pe_ratio(df)

    # 獲取其他財務數據並計算 Z-score
    financial_data = get_financial_data(str_code)
    if financial_data:
        z_value, z2_value = calculate_z_scores(financial_data)
    else:
        z_value, z2_value = 0, 0

    return z_value, z2_value, pe_ratio

def get_financial_data(str_code):
    financial_data = {}
    
    try:
        # 创建 Ticker 对象
        ticker = yf.Ticker(f"{str_code}.TW")
        
        # 获取资产负债表数据
        balance_sheet = ticker.balance_sheet
        if not balance_sheet.empty:
            balance_sheet = balance_sheet.iloc[:, 0]  # 最新季度数据
            financial_data['總資產'] = balance_sheet.get('Total Assets', 0)
            financial_data['總負債'] = balance_sheet.get('Total Liabilities Net Minority Interest', 0)
            financial_data['流動資產'] = balance_sheet.get('Current Assets', 0)
            financial_data['保留盈餘'] = balance_sheet.get('Retained Earnings', 0)
            financial_data['股東權益總額'] = balance_sheet.get('Stockholders Equity', 0)
            financial_data['股本'] = balance_sheet.get('Common Stock', 0)
            financial_data['普通股股本'] = balance_sheet.get('Common Stock', 0)  # 假设普通股股本等于股本
        
        # 获取损益表数据
        income_stmt = ticker.financials
        if not income_stmt.empty:
            income_stmt = income_stmt.iloc[:, 0]  # 最新年度数据
            financial_data['稅前淨利'] = income_stmt.get('Pretax Income', 0)
            financial_data['營業收入淨額'] = income_stmt.get('Total Revenue', 0)
        
        # 获取现金流量表数据
        cash_flow = ticker.cashflow
        if not cash_flow.empty:
            cash_flow = cash_flow.iloc[:, 0]  # 最新年度数据
            financial_data['利息費用'] = cash_flow.get('Interest Expense', 0)
        
        # 获取公司基本资料
        info = ticker.info
        shares_outstanding = info.get('sharesOutstanding', 0)
        market_price = info.get('regularMarketPrice', 0)
        
        if shares_outstanding == 0 or market_price == 0:
            # 如果无法获取数据，尝试使用其他方法
            financial_data['股票總市值'] = info.get('marketCap', 0)
        else:
            financial_data['股票總市值'] = shares_outstanding * market_price
        
        # 打印调试信息
        print(f"Shares Outstanding: {shares_outstanding}")
        print(f"Market Price: {market_price}")
        print(f"Market Cap from info: {info.get('marketCap', 0)}")
        
        # 将所有数值转换为整数
        for key, value in financial_data.items():
            financial_data[key] = int(value) if pd.notnull(value) else 0
        
        print("獲取的財務數據:", financial_data)
        return financial_data
    
    except Exception as e:
        print(f"獲取數據時發生錯誤: {e}")
        return financial_data

def calculate_z_scores(financial_data):
    try:
        # 提取所需的財務數據
        total_assets = financial_data['總資產']
        total_liabilities = financial_data['總負債']
        current_assets = financial_data['流動資產']
        retained_earnings = financial_data['保留盈餘']
        ebit = financial_data['稅前淨利'] + financial_data['利息費用']
        market_value_equity = (financial_data['股本'] + financial_data['普通股股本']) / 2
        book_value_total_liabilities = financial_data['總負債']
        sales = financial_data['營業收入淨額']

        # 計算 Z-Score (Altman Z-Score)
        z_score = (
            1.2 * ((current_assets - total_liabilities) / total_assets) +
            1.4 * (retained_earnings / total_assets) +
            3.3 * (ebit / total_assets) +
            0.6 * (market_value_equity / book_value_total_liabilities) +
            1.0 * (sales / total_assets)
        )

        # 計算 Z2-Score (修改版 Altman Z-Score)
        z2_score = (
            6.56 * ((current_assets - total_liabilities) / total_assets) +
            3.26 * (retained_earnings / total_assets) +
            6.72 * (ebit / total_assets) +
            1.05 * (market_value_equity / book_value_total_liabilities)
        )

        return round(z_score, 2), round(z2_score, 2)
    except Exception as e:
        print(f"計算 Z-Score 時發生錯誤: {e}")
        return 0, 0

def get_pe_ratio(df):
    if df.empty or '日期' not in df.columns or '本益比' not in df.columns:
        print("數據框為空或缺少必要的列")
        return 0

    def get_last_4q_period():
        today = datetime.now()
        end_date = datetime(today.year, ((today.month - 1) // 3) * 3 + 1, 1) - timedelta(days=1)
        start_date = end_date - timedelta(days=365) + timedelta(days=1)
        return start_date, end_date

    start_date, end_date = get_last_4q_period()
    
    mask = (df['日期'] > start_date) & (df['日期'] <= end_date)
    filtered_df = df.loc[mask]
    
    if filtered_df.empty:
        print("過濾後的數據框為空")
        return 0
    
    return filtered_df['本益比'].mean()

def get_recommendation(z_value, z2_value, pe_ratio):
    def if_buy_or_sell(str_period, current_close, last_close, str_type=""):
        if str_type == "":
            int_ubound1, int_ubound2 = 1, 2
            int_lbound1, int_lbound2 = 5, 6
        elif str_type == "Lohas channel":
            int_ubound1, int_ubound2 = 1, 2
            int_lbound1, int_lbound2 = 3, 4
        else:
            return "No action"

        if str_period in (int_ubound1, int_ubound2):
            if current_close < last_close:
                return "Sell"
        elif str_period in (int_lbound1, int_lbound2):
            if current_close > last_close:
                return "Buy"
        return "No action"

    # 處理 z_value 和 z2_value 可能為 0 的情況
    if z_value == 0 and z2_value == 0:
        str_period = 3  # 或者您認為合適的其他值
    elif z_value > 2.99 or z2_value > 2.6:
        str_period = 1
    elif z_value < 1.81 or z2_value < 1.1:
        str_period = 6
    else:
        str_period = 3

    # 假設我們有當前收盤價和上一個收盤價
    # 這些數據應該從其他地方獲取
    current_close = 100  # 示例值
    last_close = 98  # 示例值

    recommendation = if_buy_or_sell(str_period, current_close, last_close)

    # 添加基於 PE ratio 的額外建議
    if pe_ratio > 20:
        recommendation += " (High PE Ratio)"
    elif pe_ratio < 10:
        recommendation += " (Low PE Ratio)"

    return recommendation

def test_company(company_code):
    print(f"測試公司代碼：{company_code}")

    financial_data = get_financial_data(company_code)
    print("財務數據：", financial_data)
    
    z_value = z2_value = 0  # 初始化為 0
    
    if '總資產' in financial_data:
        print("總資產：", financial_data['總資產'])
    else:
        print("無法獲取總資產數據")

    if financial_data:
        z_value, z2_value = calculate_z_scores(financial_data)
        print(f"Z-Score: {z_value}, Z2-Score: {z2_value}")
    else:
        print("無法計算 Z-Score,因為缺少財務數據")
        print("財務數據變數:")
        for key, value in financial_data.items():
            print(f"  {key}: {value}")

    df = get_historical_price_data(company_code)
    if not df.empty:
        print("歷史價格數據形狀:", df.shape)
        print("歷史價格數據列:", df.columns)

        pe_ratio = get_pe_ratio(df)
        print(f"PE Ratio: {pe_ratio}")

        recommendation = get_recommendation(z_value, z2_value, pe_ratio)
        print(f"建議: {recommendation}")
    else:
        print("無法獲取歷史價格數據")

def get_historical_price_data(str_code):
    url = f"https://www.cnyes.com/twstock/ps_historyprice.aspx?code={str_code}"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365+180)
    params = {
        'ctl00$ContentPlaceHolder1$startText': start_date.strftime('%Y/%m/%d'),
        'ctl00$ContentPlaceHolder1$endText': end_date.strftime('%Y/%m/%d')
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        for table in tables:
            html_io = StringIO(str(table))
            df = pd.read_html(html_io)[0]
            if '日期' in df.columns:
                df['日期'] = pd.to_datetime(df['日期'])
                return df
        print("無法找到包含日期列的歷史價格數據表格")
        return pd.DataFrame()
    except Exception as e:
        print(f"獲取歷史價格數據時發生錯誤: {e}")
        return pd.DataFrame()

def get_stock_info(str_code):
    """
    獲取股票資訊的函數
    參數:
        str_code: 股票代碼 (例如: '2330')
    返回:
        dict: 包含股票資訊的字典
    """
    try:
        # 創建 Ticker 對象
        ticker = yf.Ticker(f"{str_code}.TW")
        
        # 獲取基本信息
        info = ticker.info
        if not info:
            raise ValueError("無法獲取股票基本信息")
            
        # 獲取財務數據
        financial_data = get_financial_data(str_code)
        
        # 計算 Z-Score
        z_value, z2_value = calculate_z_scores(financial_data) if financial_data else (0, 0)
        
        # 獲取當前股價和其他市場數據
        current_price = info.get('regularMarketPrice', 0)
        market_cap = info.get('marketCap', 0)
        eps = info.get('trailingEps', 0)
        
        # 計算本益比
        pe_ratio = round(current_price / eps, 2) if eps and eps != 0 else 0
        
        # 取得建議
        recommendation = get_recommendation(z_value, z2_value, pe_ratio)
        
        result = {
            "success": True,
            "code": str_code,
            "name": info.get('longName', f'Stock {str_code}'),
            "current_price": current_price,
            "change": info.get('regularMarketChange', 0),
            "change_percent": info.get('regularMarketChangePercent', 0),
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "eps": eps,
            "z_score": round(z_value, 2),
            "z2_score": round(z2_value, 2),
            "recommendation": recommendation,
            "volume": info.get('volume', 0),
            "avg_volume": info.get('averageVolume', 0),
            "high_52week": info.get('fiftyTwoWeekHigh', 0),
            "low_52week": info.get('fiftyTwoWeekLow', 0)
        }
        
        print(f"成功獲取 {str_code} 的股票資訊")
        return result
    
    except Exception as e:
        error_msg = f"獲取股票資訊時發生錯誤: {str(e)}"
        print(error_msg)
        return {
            "success": False,
            "code": str_code,
            "error": error_msg,
            "name": f"Stock {str_code}",
            "current_price": 0,
            "change": 0,
            "change_percent": 0,
            "market_cap": 0,
            "pe_ratio": 0,
            "eps": 0,
            "z_score": 0,
            "z2_score": 0,
            "recommendation": "無法取得建議",
            "volume": 0,
            "avg_volume": 0,
            "high_52week": 0,
            "low_52week": 0
        }

def get_recommendation(z_value, z2_value, pe_ratio):
    """
    根據 Z-Score、Z2-Score 和本益比給出建議
    """
    try:
        if z_value == 0 or z2_value == 0:
            return "無足夠數據提供建議"
            
        # Z-Score 分析
        if z_value > 2.99:
            z_suggestion = "財務狀況良好"
        elif z_value < 1.81:
            z_suggestion = "財務狀況需注意"
        else:
            z_suggestion = "財務狀況中等"
            
        # PE ratio 分析
        if pe_ratio == 0:
            pe_suggestion = "無法計算本益比"
        elif pe_ratio > 30:
            pe_suggestion = "本益比偏高"
        elif pe_ratio < 10:
            pe_suggestion = "本益比偏低"
        else:
            pe_suggestion = "本益比適中"
            
        return f"{z_suggestion}，{pe_suggestion}"
        
    except Exception as e:
        print(f"生成建議時發生錯誤: {str(e)}")
        return "無法生成建議"

# 測試用的主程式
if __name__ == "__main__":
    test_code = "2330"
    result = get_stock_info(test_code)
    print(json.dumps(result, ensure_ascii=False, indent=2))

