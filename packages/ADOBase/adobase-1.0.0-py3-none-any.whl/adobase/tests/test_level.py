import os
from adobase.level import ADOFAILevel
from adobase.params import LEVEL_BASE

# 使用 tkinter 文件选择器
import tkinter as tk
from tkinter import filedialog

def select_file(title, filetypes):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return file_path

if __name__ == "__main__":
    print("=== ADOBase 关卡信息查看工具 ===")
    in_path = select_file("请选择要读取的 .adofai 文件", [("ADOFAI 文件", "*.adofai"), ("所有文件", "*.*")])
    if not in_path or not os.path.isfile(in_path):
        print("未选择有效文件，程序退出。")
        exit(1)
    level = ADOFAILevel.load(in_path)
    level.remove_decoration(decoration_type="AddDecoration")
    level.export("test.json", as_original=True)
