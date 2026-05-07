import os
import sys

import tkinter as tk
from tkinter import ttk, messagebox
from src.generator import load_words, generate_test_data, create_four_choice_options_E2J, create_four_choice_options_J2E, generate_test_pdf, generate_answer_pdf

class VocabularyTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("英単語テストPDF作成ツール") # ウィンドウタイトルを指定
        self.root.geometry("400x450") # ウィンドウサイズを指定

        # 単語データの読み込み
        self.data_path = 'data/words.json'
        if not os.path.exists(self.data_path):
            messagebox.showerror("エラー", f"単語データファイルが見つかりません: {self.data_path}\nscraper.pyを実行して単語データを取得してください。")
            self.root.destroy()
            return
        
        self.all_words = load_words(self.data_path)

        # レイアウト作成
        self.create_widgets()
    
    def create_widgets(self):
        # メインフレーム
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)) # フレームをウィンドウ全体に広げる

        # 出題範囲の入力
        ttk.Label(frame, text="出題範囲の開始番号（1-1900）:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.start_index = ttk.Entry(frame, width=10)
        self.start_index.grid(row=0, column=1, sticky=tk.W)
        self.start_index.insert(0, "1") # デフォルト値を設定

        ttk.Label(frame, text="出題範囲の終了番号（1-1900）:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.end_index = ttk.Entry(frame, width=10)
        self.end_index.grid(row=1, column=1, sticky=tk.W)
        self.end_index.insert(0, "1900") # デフォルト値を設定

        # 出題数の入力
        ttk.Label(frame, text="出題する問題数:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.num_questions = ttk.Entry(frame, width=10)
        self.num_questions.grid(row=2, column=1, sticky=tk.W)
        self.num_questions.insert(0, "20") # デフォルト値を設定

        # 出題モードの選択
        ttk.Label(frame, text="出題モード:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.mode_var = tk.StringVar()
        self.mode_var.set("E2J") # デフォルト値を設定
        ttk.Radiobutton(frame, text="英語→日本語", variable=self.mode_var, value="E2J").grid(row=3, column=1, sticky=tk.W)
        ttk.Radiobutton(frame, text="日本語→英語", variable=self.mode_var, value="J2E").grid(row=4, column=1, sticky=tk.W)

        # 出題形式の選択
        ttk.Label(frame, text="出題形式:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar()
        self.format_var.set("DESC") # デフォルト値を設定
        ttk.Radiobutton(frame, text="記述式問題", variable=self.format_var, value="DESC").grid(row=5, column=1, sticky=tk.W)
        ttk.Radiobutton(frame, text="選択式問題", variable=self.format_var, value="CHOICE").grid(row=6, column=1, sticky=tk.W)

        # PDF生成ボタン
        self.generate_button = ttk.Button(frame, text="PDFを生成", command=self.generate_pdfs)
        self.generate_button.grid(row=7, column=0, columnspan=2, pady=30)

    def generate_pdfs(self):
        try:
            start_index = int(self.start_index.get())
            end_index = int(self.end_index.get())
            num_questions = int(self.num_questions.get())
            direction = self.mode_var.get()
            format = self.format_var.get()

            if start_index < 1 or end_index > 1900 or start_index >= end_index:
                messagebox.showerror("エラー", "出題範囲の番号は1から1900の間で、開始番号は終了番号未満でなければなりません。")
                return
            if num_questions < 1 or num_questions > (end_index - start_index + 1):
                messagebox.showerror("エラー", "出題する問題数は1以上で、出題範囲内の単語数を超えてはいけません。")
                return
            
            # テストデータの生成
            test_data = generate_test_data(self.all_words, start_index, end_index, num_questions)

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
            test_pdf_path = f"output/vocabulary_test_{direction}_{format}_{start_index}_{end_index}.pdf"
            answer_pdf_path = f"output/vocabulary_test_answers_{direction}_{format}_{start_index}_{end_index}.pdf"

            generate_test_pdf(test_pdf_path, final_data, direction, format)
            generate_answer_pdf(answer_pdf_path, final_data, direction, format)

            messagebox.showinfo("成功", f"PDFが生成されました:\n{test_pdf_path}\n{answer_pdf_path}")
        except ValueError:
            messagebox.showerror("エラー", "無効な入力です。数値を入力してください。")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyTestGUI(root)
    root.mainloop()