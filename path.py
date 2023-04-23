import os

#現在のディレクトリを取得
path_1 = os.getcwd()
path_2 = os.path.dirname(os.path.abspath(__file__))

print(f'path1: {path_1}\npath2: {path_2}')
#実行結果
# python
# D:\Taro\Documents\workspace\src\Twitter\twitter_get_user_id
# d:\Taro\Documents\workspace\src\Twitter\twitter_get_user_id
# Nuitka exe
# D:\Taro\Documents\workspace\src\Twitter\twitter_get_user_id
# C:\Users\hannt\AppData\Local\Temp\ONEFIL~2