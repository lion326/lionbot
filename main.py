from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
import requests

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
)
import os

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    returnmessage = event.message.text
    if event.message.text == "こんにちは":
        returnmessage = "どうもこんにちは"
    elif event.message.text == "こんばんは":
        returnmessage = "どうもこんばんは"
    elif event.message.text == "疲れた":
        returnmessage = "お疲れ様でした"
    elif event.message.text == "ネオテック":
        # 社長の画像送信
        neotecimage(event)
    elif event.message.text == "清水" or event.message.text == "松田":
        # 清水の画像送信
        matsudaimage(event)
    elif event.message.text == "犬の画像" or event.message.text == "犬" or event.message.text == "犬":
        # DogAPI
        Dogimage(event)
    # 返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=returnmessage))


def neotecimage(event):
    messages = ImageSendMessage(
        original_content_url="https://neotec-n.com/wp/wp-content/uploads/2016/07/syatyou02.jpg",
        preview_image_url="https://neotec-n.com/wp/wp-content/uploads/2016/07/syatyou02.jpg"
    )
    line_bot_api.reply_message(
        event.reply_token,
        messages)


def matsudaimage(event):
    messages = ImageSendMessage(
        original_content_url="https://neotec-n.com/wp/wp-content/uploads/2016/06/c_01.jpg",
        preview_image_url="https://neotec-n.com/wp/wp-content/uploads/2016/06/c_01.jpg"
    )
    line_bot_api.reply_message(
        event.reply_token,
        messages)


def Dogimage(event):
    api_url = "https://dog.ceo/api/breeds/image/random"
    dog_response = requests.get(api_url)
    dog_json = dog_response.json()
    dogimage_url = dog_json['message']
    messages = ImageSendMessage(
        original_content_url=dogimage_url,
        preview_image_url=dogimage_url
    )
    line_bot_api.reply_message(
        event.reply_token,
        messages)


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
