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

if __name__ == "__main__":
    # 動作テスト
    words = load_words('data/words.json')
    test_data = generate_test_data(words, 1, 100, 10)

    for i, item in enumerate(test_data, 1):
        print(f"問 {i}: {item['word']} ({item['index']}) - {item['meaning']}")