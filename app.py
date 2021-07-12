# -*- coding: utf-8 -*-
from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler, WebhookParser)

from linebot.exceptions import InvalidSignatureError

from linebot.models import *

from modules.Data_Searching import SearchingInJson 

#GOOGLE_API_KEY = 'AIzaSyBIJ4CV71YWlR_ZhqU9pmZ-vP4NuQEau_s'

app = Flask(__name__)

# load channel_access_token and channel_secret
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
#parser = WebhookParser(config.get('line-bot', 'channel_secret'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text = True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    
    try:
        print('X-LINE-SIGNATURE驗證成功')
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
    

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    district_list = [   
        "中正", "萬華", "松山", "大安", "內湖", "信義", "中山", "士林", "文山", "大同", 
        "北投" , "南港", "板橋", "中和", "永和", "新店", "土城", "新莊", "三重", "蘆洲",
        "林口", "三峽", "鶯歌", "淡水", "汐止", "泰山", "五股", "八里", "深坑"
    ]
    type_list = ["豚骨", "魚介", "煮干", "秋刀魚", "醬油", "蝶豆花", "雞骨", "拌麵", "味噌", "沾麵", "鹽味", "喜多方"]
    search = SearchingInJson()
    key = event.message.text
    if key == "所有店家": # 回傳店家列表給user
        message = "店家列表:\n"
        message += search.printallstores()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
    elif key in district_list: # 以行政區搜尋該區店家
        message = f"{key}區店家列表:\n"
        message += search.search_district(key)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
    elif key in type_list: # 以湯頭、餐點類型搜尋該店家
        message = f"{key}店家列表:\n"
        message += search.search_soup_type(key)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
    else: # 查詢是否有user 輸入的店家
        message = search.search_name(key)
        if message != "無該店家資料":
            #message = TextSendMessage(text="https://www.instagram.com/p/CLvTa5EM50e/")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
        else:
            #message = TextSendMessage(text=event.message.text)
            message = TextSendMessage(text = "查無店家資料")
            line_bot_api.reply_message(event.reply_token, message)


# 處理貼圖訊息
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    # 當有貼圖訊息傳入時
    print('*'*30)
    print('使用者傳入貼圖訊息')
    print(str(event))

    # 準備要回傳的貼圖訊息
    # HINT: 機器人可用的貼圖 https://developers.line.biz/en/docs/messaging-api/sticker-list/#sticker-definitions
    reply = StickerSendMessage(package_id='2', sticker_id='149')

    # 回傳訊息
    line_bot_api.reply_message(event.reply_token, reply)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
