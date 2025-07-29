import os
from adobase.level import ADOFAILevel

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
    print("\n【更多关卡信息】")
    level.print_info('version') 
    print("\n【编辑关卡信息】")
    level.edit_info(version="15")
    print("\n【验证修改】")
    level.print_info('version')
    print("\n【导出关卡】")
    level.export('111.json', as_original=False)
    print("\n【导出原始关卡】")
    level.export('111.adofai', as_original=True)