### Twitterのuser_idを取得するツール

#### 目的
本ツールの目的は、乗っ取り被害に備えて、Twitterのuser_idを取得することです。  
@から始まるユーザー名は、変更可能ですが、user_idはアカウントごとに固有の値です。  
そこで、user_idを取得しておくことで、アカウントが乗っ取られた場合に@usernameを  
変更されたとしても、user_idを利用することで、アカウントを特定することができます。

このツールにより一人でも多くの方が、乗っ取り被害に備えることができれば幸いです。

#### 使い方 (簡易版)
1. 「twitter_get_user_id.exe」と「chromedriver.exe」ファイルをダウンロードする
2. 「twitter_get_user_id.exe」ファイルを実行する

#### 使い方 (詳細版)
1. 「twitter_get_user_id.exe」と「chromedriver.exe」ファイルをダウンロードする
2. 「twitter_get_user_id.exe」ファイルを実行する
3. 入力ボックスにユーザー名とパスワードを入力する
4. ログインボタンを押す
5. ログイン情報が正しい場合、user_idを利用したURL等が記録される

##### 補足
- ログイン情報は、ツールの終了時に削除されるため、保持されません。
- Chromeのバージョンによっては、chromedriver.exeが動作しない場合があります。
- その場合は、Chromeのバージョンに合わせたchromedriver.exeをダウンロードしてください。
- chrome//version でChromeのバージョンを確認できます。
- 以下のサイトからChromeのバージョンに合わせたドライバーをダウンロードしてください。
- https://sites.google.com/chromium.org/driver/downloads


