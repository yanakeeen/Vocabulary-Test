import json
import random

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

# フォントの登録
pdfmetrics.registerFont(TTFont('NotoSansJP', 'fonts/NotoSansJP-Regular.ttf'))  # フォントファイルのパスを指定

def generate_test_pdf(filename, test_data, mode):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4 # 210mm x 297mm
    fontname = 'NotoSansJP'

    # ヘッダー
    c.setFont(fontname, 16)
    c.drawCentredString(width / 2, height - 20 * mm, "英単語テスト")
    c.setFont(fontname, 10)
    c.drawString(20 * mm, height - 35 * mm, "実施日: ____年__月__日")
    c.drawString(width - 90 * mm, height - 35 * mm, "氏名: ____________________")
    c.drawString(width - 30 * mm, height - 35 * mm, "得点: ____点")

    # 問題の描画

    c.save()


def load_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_test_data(words, start_index, end_index, num_questions):
    # 指定された範囲の単語をフィルタリング
    filtered_words = [word for word in words if start_index <= int(word['index']) <= end_index]

    # 指定された問題数が範囲内の単語数を超えている場合は、範囲内の単語数に合わせる
    if num_questions > len(filtered_words):
        num_questions = len(filtered_words)

    # ランダムに問題を選択
    selected_words = random.sample(filtered_words, num_questions)
    return selected_words

# 英→日の4択問題を作成
def create_four_choice_options_E2J(correct_word, all_words_in_range, num_options=4):
    # 正解以外の選択肢をランダムに選ぶ
    incorrect_pool = [word['meaning'] for word in all_words_in_range if word['word'] != correct_word['word']]
    incorrect_options = random.sample(incorrect_pool, min(num_options - 1, len(incorrect_pool))) # 4択にできない場合は、可能な限り選択肢を作成

    options = incorrect_options + [correct_word['meaning']] # 正解の選択肢を追加
    random.shuffle(options)  # 選択肢をシャッフル

    correct_index = options.index(correct_word['meaning'])  # 正解の選択肢のインデックスを取得
    labels = ['A', 'B', 'C', 'D'][:len(options)]  # 選択肢のラベルを作成（4択に満たない場合は、必要な分だけラベルを使用）

    return {
        'word': correct_word['word'],
        'options': options,
        'answer_label': labels[correct_index],
        'answer_meaning': correct_word['meaning']
    }

# 日→英の4択問題を作成
def create_four_choice_options_J2E(correct_word, all_words_in_range, num_options=4):
    # 正解以外の選択肢をランダムに選ぶ
    incorrect_pool = [word['word'] for word in all_words_in_range if word['meaning'] != correct_word['meaning']]
    incorrect_options = random.sample(incorrect_pool, min(num_options - 1, len(incorrect_pool))) # 4択にできない場合は、可能な限り選択肢を作成

    options = incorrect_options + [correct_word['word']] # 正解の選択肢を追加
    random.shuffle(options)  # 選択肢をシャッフル

    correct_index = options.index(correct_word['word'])  # 正解の選択肢のインデックスを取得
    labels = ['A', 'B', 'C', 'D'][:len(options)]  # 選択肢のラベルを作成（4択に満たない場合は、必要な分だけラベルを使用）

    return {
        'meaning': correct_word['meaning'],
        'options': options,
        'answer_label': labels[correct_index],
        'answer_word': correct_word['word']
    }

if __name__ == "__main__":
    # 動作テスト
    words = load_words('data/words.json')
    test_data = generate_test_data(words, 1, 100, 10)

    # for word in test_data:
    #     options = create_four_choice_options_J2E(word, words)
    #     print(f"問: {options['meaning']}")
    #     for label, option in zip(['A', 'B', 'C', 'D'], options['options']):
    #         print(f"{label}: {option}")
    #     print(f"正解: {options['answer_label']} ({options['answer_word']})")
    #     print()

    # PDF生成のテスト
    generate_test_pdf('output/test_header.pdf', test_data, mode='E2J')