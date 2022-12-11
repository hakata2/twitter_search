# twitter_search

## 概要
本プログラムはユーザが指定したキーワードをtwitterで検索します。  
（キーワード毎に最新の10件が取得されます。10件はTwitterのデフォルトであり、件数を変更する場合はAPI指定に件数を追加して下さい。）  
前回実行時以降に新規投稿されたツイートをLINEに通知します。
（前回実行時の通知済みツイートのIDは、maxidファイルにて管理）

## 事前準備
1. twitter APIとLINE Notifyを利用するためのキーを取得
2. getTwitter.pyと同一ディレクトリ内に以下内容のkeys.pyを作成し、xxxを上記で取得したキーに置き換える。
```
### Twitter ###
# OAuth2.0 ClientID and ClientSecret
CLIENT_ID = "xxx"
CLIENT_SECRET = "xxx"

# ConsumerKey
API_KEY = "xxx"
API_KEY_SECRET = "xxx"

# Authentication Tokens
TWITTER_BEARER_TOKEN = "xxx"
TWITTER_ACCESS_TOKEN = "xxx"
TWITTER_ACCESS_TOKEN_SECRET = "xxx"


### Line Notify ###
LINE_NOTIFY_TOKEN = 'xxx'
```
3. settings.pyを編集し、通知対象キーワードを変更
* KEYWORDS: 検索ワード1
* SUB_KEYWORDS: 検索ワード1にAND条件で加える検索ワード(検索ワード1と2の全ての組み合わせを検索します。)
* BLACKLIST: 検索結果のツイートに本キーワードが一つでも含まれる場合に通知対象外にします。

## 実行方法
以下コマンドで実行
```
python getTweet.py
```
定期実行する場合は以下コマンドを実行(実行間隔はスクリプト内のTIMEの値を変更してください。（単位：秒）)
```
sh exec.sh
```
