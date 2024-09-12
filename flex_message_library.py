from venv import logger


def create_stock_flex_message(stock_info):
    logger.debug(f"創建股票 Flex Message，輸入數據: {stock_info}")
    try:
        if "error" in stock_info:
            return {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "獲取股票信息失敗",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#ff0000"
                        },
                        {
                            "type": "text",
                            "text": stock_info["error"],
                            "wrap": True
                        }
                    ]
                }
            }

        flex_content = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"{stock_info['股票名稱']} ({stock_info['股票代碼']})", "weight": "bold", "size": "xl"},
                    {"type": "text", "text": f"日期: {stock_info['日期']}", "size": "sm", "color": "#888888"},
                    {"type": "separator", "margin": "xxl"},
                    {"type": "box", "layout": "vertical", "margin": "xxl", "spacing": "sm", "contents": [
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "收盤價", "size": "sm", "color": "#555555", "flex": 0},
                            {"type": "text", "text": stock_info['收盤價'], "size": "sm", "color": "#111111", "align": "end"}
                        ]},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "漲跌價差", "size": "sm", "color": "#555555", "flex": 0},
                            {"type": "text", "text": stock_info['漲跌價差'], "size": "sm", "color": "#111111", "align": "end"}
                        ]},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "漲跌幅", "size": "sm", "color": "#555555", "flex": 0},
                            {"type": "text", "text": stock_info['漲跌幅'], "size": "sm", "color": "#111111", "align": "end"}
                        ]},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "開盤價", "size": "sm", "color": "#555555", "flex": 0},
                            {"type": "text", "text": stock_info['開盤價'], "size": "sm", "color": "#111111", "align": "end"}
                        ]},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "最高價", "size": "sm", "color": "#555555", "flex": 0},
                            {"type": "text", "text": stock_info['最高價'], "size": "sm", "color": "#111111", "align": "end"}
                        ]},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "最低價", "size": "sm", "color": "#555555", "flex": 0},
                            {"type": "text", "text": stock_info['最低價'], "size": "sm", "color": "#111111", "align": "end"}
                        ]},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "成交股數", "size": "sm", "color": "#555555", "flex": 0},
                            {"type": "text", "text": stock_info['成交股數'], "size": "sm", "color": "#111111", "align": "end"}
                        ]},
                        {"type": "box", "layout": "horizontal", "contents": [
                            {"type": "text", "text": "成交金額", "size": "sm", "color": "#555555", "flex": 0},
                            {"type": "text", "text": stock_info['成交金額'], "size": "sm", "color": "#111111", "align": "end"}
                        ]}
                    ]}
                ]
            }
        }
        logger.debug("成功創建 Flex Message")
        return flex_content
    except Exception as e:
        logger.exception("創建 Flex Message 時發生錯誤")
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "創建 Flex Message 時發生錯誤",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#ff0000"
                    },
                    {
                        "type": "text",
                        "text": str(e),
                        "wrap": True
                    }
                ]
            }
        }