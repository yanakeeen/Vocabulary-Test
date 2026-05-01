import os
import sys

from src.generator import load_words, generate_test_data, create_four_choice_options_E2J, create_four_choice_options_J2E, generate_test_pdf, generate_answer_pdf

def main():
    print("英単語テストPDFジェネレーター")

    # 単語データの読み込み
    data_path = 'data/words.json'
    if not os.path.exists(data_path):
        print(f"エラー: 単語データファイルが見つかりません: {data_path}")
        print("scraper.pyを実行して単語データを取得してください。")
        sys.exit(1)
    
    all_words = load_words(data_path)

    # ユーザーからの入力を取得
    try:
        start_index = int(input("出題範囲の開始番号（1-1900）："))
        end_index = int(input("出題範囲の終了番号（1-1900）："))
        num_questions = int(input("出題する問題数："))

        print()
        print("出題モードの選択")
        print("1: 英→日（記述式）")
        print("2: 英→日（選択式）")
        print("3: 日→英（記述式）")
        print("4: 日→英（選択式）")
        mode_number = int(input("モードを選択してください（1-4）："))

        if mode_number == 1:
            direction = 'E2J'
            format = 'DESC'
        elif mode_number == 2:
            direction = 'E2J'
            format = 'CHOICE'
        elif mode_number == 3:
            direction = 'J2E'
            format = 'DESC'
        elif mode_number == 4:
            direction = 'J2E'
            format = 'CHOICE'
        else:
            print("無効なモードが選択されました。1から4の数字を入力してください。")
            sys.exit(1)
        
    except ValueError:
        print("無効な入力です。数値を入力してください。")
        sys.exit(1)
    
    if start_index < 1 or end_index > 1900 or start_index >= end_index:
        print("出題範囲の番号は1から1900の間で、開始番号は終了番号未満でなければなりません。")
        sys.exit(1)

    # テストデータの生成
    print("テストデータを生成しています...")
    test_data = generate_test_data(all_words, start_index, end_index, num_questions)

    # 選択式の問題データを作成
    final_data = []
    if format == 'CHOICE':
        for word in test_data:
            if direction == 'E2J':
                final_data.append(create_four_choice_options_E2J(word, test_data))
            else:
                final_data.append(create_four_choice_options_J2E(word, test_data))
    else:
        final_data = test_data
    
    # PDFの生成
    print("PDFを生成しています...")
    test_pdf_path = f'output/test_{direction}_{format}_{start_index}-{end_index}.pdf'
    answer_pdf_path = f'output/answer_{direction}_{format}_{start_index}-{end_index}.pdf'

    generate_test_pdf(test_pdf_path, final_data, direction=direction, format=format)
    generate_answer_pdf(answer_pdf_path, final_data, direction=direction, format=format)

    print(f"テストPDFが生成されました: {test_pdf_path}")
    print(f"解答PDFが生成されました: {answer_pdf_path}")

if __name__ == "__main__":
    main()
        