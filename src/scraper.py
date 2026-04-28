import requests
from bs4 import BeautifulSoup
import json
import os
import time

def scrape_words(url):
    # ユーザーエージェントの設定
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # ウェブページにアクセスしてHTMLを取得
        response = requests.get(url, headers=headers)
        response.raise_for_status() # HTTPエラーが発生した場合は例外をスロー
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
        return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')  # BeautifulSoupを使用してHTMLを解析
    # データ処理ロジックをここに追加
    return soup

if __name__ == "__main__":
    target_url = "https://ukaru-eigo.com/target-1900-word-list/"  # スクレイピングしたいURLを入力

    print("データを取得中...")
    html = scrape_words(target_url)

    # 取得したHTMLが存在する場合
    if html:
        data = parse_html(html)
        os.makedirs('data', exist_ok=True)  # データ保存用のディレクトリを作成

        with open('data/words.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)  # データをJSON形式で保存

        print(f"{len(data)}件のデータを保存しました。")