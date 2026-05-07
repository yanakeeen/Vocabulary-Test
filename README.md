# Vocabulary Test Generator

## 概要
自分や塾の生徒用の単語小テスト作成ツール
ウェブから単語データを取得し、PDF形式で小テストを作成

## 主な機能
- [x] ウェブからの単語データ自動取得
- [x] 4種の出題形式(日→英、英→日と記述、四択)
- [x] 印刷用にPDF形式で出力
- [x] GUI(開発予定)

## 技術スタック
- Python 3.8.10
- requests/BeautifulSoup4 (Scraping)
- Reportlab 3.6.13 (PDF Generation)
- Tkinter

## 開発ロードマップ
1. 単語の取得とデータ処理の実装
2. PDF出力の実装
3. GUI版の実装