import PyInstaller.__main__
import os
import sys

# 1. 設定你的主程式檔案名稱
ENTRY_POINT = "main.py"  # 請確認這是你的主程式檔名

# 2. 設定打包後的執行檔名稱
APP_NAME = "LostEarthKeys"

# 3. 處理路徑分隔符號 (Windows用分號';', Mac/Linux用冒號':')
path_sep = ';' if os.name == 'nt' else ':'

# 4. 定義要打包的資源資料夾
# 格式: '來源資料夾路徑' + path_sep + '目標資料夾名稱'
# 我們要把整個 assets 資料夾放進去
add_data_assets = 'assets' + path_sep + 'assets'

# 如果你有其他的設定檔(非.py)或字型，也要加進去
# 例如: add_data_ver1 = 'ver1' + path_sep + 'ver1' (如果 ver1 包含初始存檔)

# 5. PyInstaller 參數設定
args = [
    ENTRY_POINT,  # 主程式
    f'--name={APP_NAME}',  # 執行檔名稱
    '--onefile',  # 打包成單一執行檔 (.exe)
    '--windowed',  # 執行時不顯示黑色終端機視窗 (No Console)
    '--clean',  # 清除快取
    f'--add-data={add_data_assets}',  # 加入 assets 資料夾 (關鍵！)

    # 如果 sprites 或 settings 沒有被自動偵測到 (通常 import 了就會有，但在這裡強制加入路徑確保萬無一失)
    '--paths=.',

    # 選擇性：如果有 icon 圖示，請取消下一行的註解並修改路徑
    # '--icon=assets/icon.ico',
]

print("開始打包...")
print(f"執行參數: {args}")

# 執行 PyInstaller
PyInstaller.__main__.run(args)

print("=" * 30)
print(f"打包完成！請檢查 'dist' 資料夾內的 {APP_NAME}.exe")
print("=" * 30)
