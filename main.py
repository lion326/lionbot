from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
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
    # 返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=returnmessage))


def neotecimage(event):
    # messages = ImageSendMessage(
    #     # JPEG 最大画像サイズ：240×240 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
    #     original_content_url="http://neotec-n.com/wp/wp-content/uploads/2016/07/syatyou02.jpg",
    #     # JPEG 最大画像サイズ：1024×1024 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
    #     preview_image_url="http://neotec-n.com/wp/wp-content/uploads/2016/07/syatyou02.jpg"
    # )
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     messages)
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url="https://1.bp.blogspot.com/-7uiCs6dI4a0/YEGQA-8JOrI/AAAAAAABddA/qPFt2E8vDfQwPQsAYLvk4lowkwP-GN7VQCNcBGAsYHQ/s896/buranko_girl_smile.png",
            preview_image_url="https://1.bp.blogspot.com/-7uiCs6dI4a0/YEGQA-8JOrI/AAAAAAABddA/qPFt2E8vDfQwPQsAYLvk4lowkwP-GN7VQCNcBGAsYHQ/s896/buranko_girl_smile.png"))


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
