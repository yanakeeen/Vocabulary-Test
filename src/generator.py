import json
import random

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

def create_four_choice_options(correct_word, all_words_in_range, num_options=4):
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


if __name__ == "__main__":
    # 動作テスト
    words = load_words('data/words.json')
    test_data = generate_test_data(words, 1, 100, 10)

    for word in test_data:
        options = create_four_choice_options(word, words)
        print(f"問: {options['word']}")
        for label, option in zip(['A', 'B', 'C', 'D'], options['options']):
            print(f"{label}: {option}")
        print(f"正解: {options['answer_label']} ({options['answer_meaning']})")
        print()