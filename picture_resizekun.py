#画像をリサイズするプログラム
import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image

#メインウィンドウ
root = tk.Tk()
root.title("画像リサイズくん")
root.geometry("600x500")

#入力フォルダ選択
def select_input_folder():
    folder = filedialog.askdirectory()
    if folder:
        input_folder_var.set(folder)

#出力フォルダ選択
def select_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_folder_var.set(folder)

#リサイズ関数
def resize_image():
    size_text = size_var.get()

    #例："800x600"を分割して幅と高さを取得
    if "x" not in size_text:
        log_text.delete("1.0",tk.END) #ログのクリア
        log_text.insert(tk.END,"⚠️サイズの形式が不正です。例：800x600\n")
        return
    
    try:
        width_str, height_str = size_text.lower().split("x")
        width = int(width_str)
        height = int(height_str)
        print(f"幅：{width}, 高さ：{height}")
    except ValueError:
        log_text.delete("1.0", tk.END)
        log_text.insert(tk.END, "⚠️数値に変換できませんでした。")
        return
    
    #入力・出力フォルダ確認
    input_dir = input_folder_var.get()
    output_dir = output_folder_var.get()

    #入力フォルダの中身を確認
    if not os.path.isdir(input_dir):
        log_text.delete("1.0", tk.END)
        log_text.insert(tk.END,"⚠️入力フォルダが指定されていません。")
        return
    
    #出力フォルダの中身を確認
    if not os.path.isdir(output_dir):
        log_text.delete("1.0", tk.END)
        log_text.insert(tk.END, "⚠️出力フォルダが指定されていません。")
        return
    
    #ログクリア
    log_text.delete("1.0", tk.END)

    #対象画像を抽出（jpg, png, jepgのみ）
    image_extensions =(".jpg", ".png", ".jepg")
    image_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith(image_extensions)
    ]

    #デバッグ用に一覧表示
    print("取得した画像ファイル：")
    for img in image_files:
        print("・", img)

    if not image_files:
        print("⚠️指定フォルダに画像が見つかりませんでした。")
        return
     
    #リサイズ＆保存処理
    for img_path in image_files:
        try:
            with Image.open(img_path) as img:
                #アスペクト比を保ったまま指定サイズに収まるようにリサイズ
                img.thumbnail((width, height)) #ここで比率保持してリサイズ

                #保存先のパスを作成
                filename = os.path.basename(img_path)
                save_path = os.path.join(output_dir, filename)

                #画像を保存
                img.save(save_path)
                log_text.insert(tk.END,f"✅️保存完了：{save_path}\n")

        except Exception as e:
            log_text.insert(tk.END, f"⚠️エラー：{img_path} → {e}\n")

    log_text.insert(tk.END, "\n🎉 すべての画像を保存しました！")

#各種変数
input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()
size_var = tk.StringVar(value="800x600")


# UI配置
tk.Label(root, text="入力フォルダ：").grid(row=0, column=0, sticky="e", padx=10, pady=10)
tk.Entry(root, textvariable=input_folder_var, width=40).grid(row=0, column=1)
tk.Button(root, text="選択", command=select_input_folder).grid(row=0, column=2)

tk.Label(root, text="出力フォルダ：").grid(row=1, column=0, sticky="e", padx=10, pady=10)
tk.Entry(root, textvariable=output_folder_var, width=40).grid(row=1, column=1)
tk.Button(root, text="選択", command=select_output_folder).grid(row=1, column=2)

tk.Label(root, text="サイズ（例：800x600）：").grid(row=2, column=0, sticky="e", padx=10, pady=10)
tk.Entry(root, textvariable=size_var, width=20).grid(row=2, column=1, sticky="w")

#実行ボタン
tk.Button(root, text="実行", width=15, height=2, command=resize_image).grid(row=4, column=1, pady=30)

#テキストログ
log_text = tk.Text(root, height=15, width=70)
log_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

#メインループ
root.mainloop()
