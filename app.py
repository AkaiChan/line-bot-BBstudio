import os
import requests
import psycopg2
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])
OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']  # 請確保設置這個環境變數

# 資料庫連接函數
def get_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=zh_tw"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"{city}的天氣：{weather_description}，溫度：{temperature}°C"
    else:
        return "抱歉，無法獲取天氣資訊。"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    if '|' in user_message:
        # 分割訊息
        call, response = user_message.split('|', 1)
        call = call.strip()
        response = response.strip()
        
        # 儲存到資料庫
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO callmemory (call, response) VALUES (%s, %s)", (call, response))
            conn.commit()
            cur.close()
            conn.close()
            reply_text = f"已儲存：\n呼叫: {call}\n回應: {response}"
        except Exception as e:
            print(f"資料庫錯誤: {e}")
            reply_text = "儲存失敗，請稍後再試。"
    else:
        # 原有的邏輯
        if user_message == "哈囉":
            reply_text = "你好嗎？"
        elif "天氣" in user_message:
            city = "台北"  # 預設城市，您可以根據需要修改
            reply_text = get_weather(city)
        else:
            reply_text = user_message
    
    message = TextSendMessage(text=reply_text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)