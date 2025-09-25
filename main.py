import os
import re
import json
import random
from googleapiclient.discovery import build

def get_live_id_from_url(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if not match:
        raise ValueError("URLからライブIDが取得できません")
    return match.group(1)

def send_comment(youtube, live_id, message):
    youtube.liveChatMessages().insert(
        part="snippet",
        body={
            "snippet": {
                "liveChatId": live_id,
                "type": "textMessageEvent",
                "textMessageDetails": {"messageText": message}
            }
        }
    ).execute()

def log_message(msg):
    print(msg)
    with open("comment_log.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def set_proxy_env(proxy_file):
    with open(proxy_file, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
    if not proxies:
        return
    proxy = proxies[0] 
    os.environ["HTTP_PROXY"] = f"http://{proxy}"
    os.environ["HTTPS_PROXY"] = f"http://{proxy}"
    print(f"プロキシ設定: {proxy}")

# 主な処理

# 設定読み込み
with open("config.json") as f:
    config = json.load(f)

# proxy
if config.get("use_proxy"):
    set_proxy_env(config.get("proxy_file"))

# 情報読み込み
with open("accounts.json") as f:
    accounts = json.load(f)

# コメントリスト読み込み
with open("comments.txt") as f:
    comments = [line.strip() for line in f if line.strip()]

# ライブURLからID取得
live_url = input("ライブURLを入力してください: ")
live_id = get_live_id_from_url(live_url)

# コメント順序設定
if config.get("comment_order") == "random":
    random.shuffle(comments)

# コメント送信ループ
for acc in accounts:
    youtube = build("youtube", "v3", credentials=acc["token"])
    for comment in comments:
        success = False
        for attempt in range(config.get("retry_on_fail", 1)):
            try:
                if config.get("test_mode", True):
                    log_message(f"[テストモード] {acc['name']} -> {comment}")
                else:
                    send_comment(youtube, live_id, comment)
                    log_message(f"{acc['name']} -> {comment}")
                success = True
                break
            except Exception as e:
                log_message(f"失敗: {acc['name']} -> {comment} | リトライ {attempt+1} | エラー: {e}")
        if not success:
            log_message(f"最終的に失敗: {acc['name']} -> {comment}")
