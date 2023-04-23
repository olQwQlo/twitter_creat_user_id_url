#seleniumを用いてTwitterにログインする
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re
import os
import random
#GUIを表示する
import threading

from tkinter import *
from tkinter import ttk
from tkinter import messagebox


#ブラウザを初期化する
def get_driver():
    """
    ブラウザを初期化する

    Returns:
        selenium.webdriver.chrome.webdriver.WebDriver: ブラウザのウィンドウ

    Example:
        >>> driver = init_browser()

    Dependencies:
        - os
        - random
        - time
        - selenium.webdriver.chrome.webdriver.WebDriver
    """
    options = webdriver.ChromeOptions()
    # profileをしないことにより、毎回初期化される
    options.add_argument('--no-first-run')  # 最初の実行時のダイアログを非表示にする
    options.add_argument('--no-default-browser-check')  # デフォルトのブラウザチェックを無効にする
    #画面サイズを指定する
    options.add_argument('--window-size=700,700')
    # エージェントを切り替える
    agents = {
        "Windows_chrome_1": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "windows_chrome_2": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "windows_edge_1": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34",
        "windows_edge_2": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
    }
    key_list = list(agents.keys())
    #ランダムなagentをオプションに設定
    #乱数のシードを設定
    random.seed(time.time())
    key = key_list[random.randint(0, len(key_list) - 1)]
    agent = agents[key]
    print("UA: " + agent)
    options.add_argument('--user-agent=' + agent)
    # ChromeDriverが更新により動かなくなった場合は、以下のURLから最新のバージョンをダウンロードする
    # https://sites.google.com/chromium.org/driver/downloads
    # ダウンロードしたファイルをこのディレクトリに配置する
    try:
        driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
    except:
        print('ChromeDriverが非対応または存在しません')
        print('chrome://version でバージョンを確認してください')
        print('対応するChromeDriverをダウンロードし、このディレクトリに配置してください')
        print('https://sites.google.com/chromium.org/driver/downloads')
        return None
    return driver


# Twitterにログインする
def login_twitter(driver: webdriver.Chrome, username: str, password: str):
    """
    Twitterにログインする関数。

    Parameters:
    -----------
    driver : webdriver.Chrome
        WebDriverのインスタンス。

    Returns:
    --------
    driver : webdriver.Chrome
        ログイン後のWebDriverのインスタンス。ログインに失敗した場合はNoneを返す。
    """

    # Twitterのhomeページを開く
    driver.get("https://twitter.com/home")
    try:#リダイレクトされるか確認
        WebDriverWait(driver, 3).until(EC.url_changes(driver.current_url))
    except:
        if driver.current_url == "https://twitter.com/home":
            print("ログイン済みです")
            return driver
    # Twitterのログインページを開く
    print("ログインが必要です")
    driver.get("https://twitter.com/i/flow/login")

    #ユーザーネームの入力
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
    username_input = driver.find_element(By.NAME, "text")
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)
    #ユーザーネームまたはパスワードが間違っているとき
    #エラーが生じるのでブラウザを閉じる
    print("ユーザーネームを入力しました")
    try:
        #パスワードの入力
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "password")))
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        print("パスワードを入力しました")
    except:
        print("ユーザーネームまたはパスワードが間違っています")
        driver.quit()
        return None
    #「認証コード」の文字列がspanタグに出現するまで待機
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '認証コード')]")))
    except:
        print("認証コードは不要です")
    else:
        print('ブラウザに直接入力してください')
        WebDriverWait(driver, 120).until(EC.url_changes(driver.current_url))    
    print('ログイン情報の入力が完了しました')

    driver.get("https://twitter.com/home")
    # urlが変わらないか待機して確認
    try:
        WebDriverWait(driver, 3).until(EC.url_changes(driver.current_url))
    except:
        pass

    # ログインに成功したか確認
    if driver.current_url == 'https://twitter.com/home':
        print('ログインに成功しました')
        return driver
    
    elif driver.current_url == 'https://twitter.com/account/access':
            # reCAPTCHA認証にリダイレクトさせられた場合
            print('reCAPTCHA認証にリダイレクトされました')
            print('手動で認証を行ってください')
            input('認証を完了させ、いずれかのキーを押してください')
            if driver.current_url == 'https://twitter.com/home':
                print('ログインに成功しました')
                return driver
            else:
                print('認証が未完了です')
                print('もう一度待機します。\nホーム画面に遷移してから、いずれかのキーを押してください')
                input('認証を完了させ、いずれかのキーを押してください')
                if driver.current_url == 'https://twitter.com/home':
                    print('ログインに成功しました')
                    return driver
            print('認証に失敗しました')
    else:
        print('不明なURLです')
        print(f'URL: {driver.current_url}')
    
    # ログインに失敗した場合
    print('ログインに失敗しました')
    print('ブラウザを終了します')
    driver.quit()
    return None


#HTMLからstr_idを探索する
def get_twitter_user_id(driver: webdriver.Chrome, username: str) -> str:
    """
    TwitterのユーザーIDを取得する関数。

    Returns:
    --------
    str_id : str
        ユーザーID。
    """
    #Twitterのホーム画面を開く
    print("ホーム画面を開きます")
    driver.get(f'https://twitter.com/{username}')
    #ユーザーIDが表示されるまで待機
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//script[contains(text(),"window.__INITIAL_STATE__")]')))
    # スクリプト要素を取得
    print('ページ要素を取得中です')
    script_element = driver.find_element(By.XPATH, '//script[contains(text(),"window.__INITIAL_STATE__")]')
    script_text = script_element.get_attribute("innerHTML")
    initial_state = script_text.split("window.__INITIAL_STATE__=")[1].replace(";", "")
    print('ページ要素の取得が完了しました')
    #str_idを取得
    #re.search()で正規表現にマッチした文字列を取得
    #"user_id":"数字"の部分を取得
    str_id_text = re.search(r'"user_id":"\d+"', initial_state).group()
    #アカウントの作成日時を取得
    # "created_at":"2023-04-17T10:07:06.000Z"の部分を取得
    create_at_text = re.search(r'"created_at":"\d{4}-\d{2}-\d{2}', initial_state).group()
    # "yyyy-MM-dd"の部分を取得
    create_at = re.search(r'\d{4}-\d{2}-\d{2}', create_at_text).group()
    #数字の部分を取得
    str_id = re.search(r'\d+', str_id_text).group()
    print(f"str_id: {str_id}")
    print(f"create_at: {create_at}")
    print("ユーザーIDの取得が完了しました")
    return str_id, create_at











def main():
    """ログイン情報を取得する
    
    Returns:
        list: ログイン情報のリスト
    """
    #GUIを表示する
    root = Tk()
    root.title("ログイン情報の入力")
    root.geometry("400x300")
    root.resizable(False, False)
    #ラベルを作成
    label1 = ttk.Label(root, text="ユーザー名を入力してください")
    label1.place(x=10, y=10)
    label2 = ttk.Label(root, text="パスワードを入力してください")
    label2.place(x=10, y=60)
    #テキストボックスを作成
    username = StringVar()
    username_entry = ttk.Entry(root, textvariable=username)
    username_entry.place(x=10, y=35)
    password = StringVar()
    password_entry = ttk.Entry(root, textvariable=password, show="*")
    password_entry.place(x=10, y=85)
    # selenium用の関数とthreadを定義
    def selenium_thread():
        try:
            username_str = username.get()
            password_str = password.get()
            driver = get_driver()
            if driver is not None:
                print('ログイン処理を開始します')
                driver = login_twitter(driver, username_str, password_str)
                print('ログイン処理を完了しました')
            if driver is not None:
                print('ユーザーIDを取得を開始します')
                str_id,create_at = get_twitter_user_id(driver, username_str)
                print('ユーザーIDを取得を完了しました')
                #user_idをもとにユーザーページへのURLを作成
                # https://twitter.com/i/user/:user_id
                user_url = f'https://twitter.com/i/user/{str_id}'
                #urlを保存する
                print('ファイルに取得情報を保存します')
                file_path = f'{os.getcwd()}\{username_str}.txt'
                print(f"保存先: {file_path}")
                with open(file_path, mode='w') as f:
                    f.write(f'username  :{username_str}\n')
                    f.write(f'create_at :{create_at}\n')
                    f.write(f'user_id   :{str_id}\n')
                    f.write(f'user_url  :{user_url}\n')
                print('保存が完了しました')
        except Exception as e:
            print(e)
        finally:
            if driver is not None:
                driver.quit()
            #ログインボタンを有効化
            login_button["state"] = "normal"




    
    #ログイン処理
    def login():
        
        """ログインボタンを押した時の処理"""
        #ユーザー名とパスワードを取得
        username_str = username.get()
        password_str = password.get()
        #ユーザー名とパスワードが空欄でないか確認
        if username_str == "" or password_str == "":
            messagebox.showerror("エラー", "ユーザー名とパスワードを入力してください")
        else:
            #ログインボタンを無効化
            login_button["state"] = "disabled"
            # #selenium用のthreadを設定
            thread = threading.Thread(target=selenium_thread)
            thread.start()

    #ログインボタンを作成
    login_button = ttk.Button(root, text="ログイン", command=login)
    login_button.place(x=10, y=120)
    root.mainloop()


if __name__ == "__main__":
    #mainループ
    main()