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
    rows = soup.find_all('tr')  # テーブルの行をすべて取得
    i=0
    for row in rows:
        cells = row.find_all('td')  # 行のセルをすべて取得

        if len(cells) >= 4:  # セルが4つ以上ある場合
            index = cells[1].get_text(strip=True)  # インデックスを取得
            word = cells[2].get_text(strip=True)  # 単語を取得
            meaning = cells[3].get_text(strip=True)  # 意味を取得
            if i<10:
                print(f"インデックス: {index}, 単語: {word}, 意味: {meaning}")  # インデックス、単語、意味を表示
            i += 1
    # データ処理ロジックをここに追加
    return soup

if __name__ == "__main__":
    target_url = "https://ukaru-eigo.com/target-1900-word-list/"  # スクレイピングしたいURLを入力

    print("データを取得中...")
    html = scrape_words(target_url)

    # 取得したHTMLが存在する場合
    if html:
        data = parse_html(html)
        # os.makedirs('data', exist_ok=True)  # データ保存用のディレクトリを作成

        # with open('data/words.json', 'w', encoding='utf-8') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)  # データをJSON形式で保存

        print(f"{len(data)}件のデータを保存しました。")


# get_text()によってテキストのみ抜き出し、タグを削除している。strip=Trueは前後の空白を削除するオプション。