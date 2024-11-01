import time
import requests
import re
import os
import threading

# 设置网址和Telegram API的token、chat_id
url = os.environ.get('URL', 'https://')
telegram_bot_token = os.environ.get('TELE_TOKEN', '')
chat_id = os.environ.get('CHAT_ID', '')


def get_account_count():
    try:
        # 获取页面内容
        response = requests.get(url)
        response.raise_for_status()

        # 使用正则表达式提取用户数量
        match = re.search(
            r'<span class="button is-large is-flexible">.*?<i class="fa fa-fw fa-users"></i> &nbsp;\s*(\d+)\s*/',
            response.text, re.DOTALL)
        if match:
            return match.group(1)
    except requests.RequestException as e:
        print(f"请求错误: {e}")
    return None


def send_telegram_message(account_count):
    message = f"当前服务器已创建账户数：{account_count}"
    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(telegram_url, data=payload)
        response.raise_for_status()
        print("消息发送成功")
    except requests.RequestException as e:
        print(f"发送Telegram消息出错: {e}")

def my_task():
    account_count = get_account_count()
    if account_count:
        send_telegram_message(account_count)
    else:
        print("未能获取到账户数量，检查页面结构是否更改")

def start_timer(interval):
    my_task()
    threading.Timer(interval, start_timer, [interval]).start()

if __name__ == '__main__':
    start_timer(3600)