# -*- coding: utf-8 -*-

from decimal import Decimal
from datetime import datetime as dt
from datetime import timedelta

import keys
import settings
# for Twitter
import json
import urllib3
# for Line
import requests

def notify_line(message):
    headers = {'Authorization': f'Bearer {keys.LINE_NOTIFY_TOKEN}'}
    data = {'message': message}
    requests.post(settings.LINE_NOTIFY_URL, headers = headers, data = data)

def get_maxid():
    maxid = 0
    f = open('maxid', 'r')
    maxid = Decimal(f.read())
    f.close()
    return maxid

def update_maxid(id):
    f = open('maxid', 'w')
    f.write(str(id) + '\n')
    f.close()

def get_newestid(data):
    # メタ情報が含まれているか確認
    if('meta' not in data):
        print('meta not found.')
        return -1

    # 当該キーワードのヒット件数確認
    if(int(data['meta']['result_count']) == 0):
        return -1
    
    return Decimal(data['meta']['newest_id'])

def check_data(data, current_id, keystr):
    notify_cnt = 0

    # 新しい投稿をLINE通知
    # recent apiは10件取得されるため、過去の投稿は通知スキップする。
    if('data' not in data):
        print('data not found.')
        return notify_cnt
    
    for tweet in data['data']:
        id = Decimal(tweet['id'])
        
        # 過去ツイートは通知対象外
        if(id <= current_id):
            continue

        # ブラックリスト内のワードを含むツイートは通知対象外
        skip = False
        for black in settings.BLACKLIST:
            if(black in tweet['text']):
                skip = True
                break

        if(skip):
            continue

        # 投稿時刻取得
        created_at = dt.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        created_at = created_at + timedelta(hours=9)

        message = '\n' + keystr + '\n' + str(created_at) + '\n' + tweet['text']
        notify_line(message)
        #print(message)
        notify_cnt = notify_cnt + 1

    return notify_cnt

def get_tweet(http, params, current_id):
    maxid = current_id
    keystr = '検索キー[' + params['query'] + ']'

    resp = http.request(
        'GET',
        settings.RECENT_SEARCH_URL,
        headers={'Authorization': 'Bearer ' + keys.TWITTER_BEARER_TOKEN},
        fields=params
    )

    data = json.loads(resp.data)

    # HTTP Req実行結果確認
    if(resp.status != 200):
        print('HTTPエラー ステータスコード：' + str(resp.status) + '(' + resp.reason + ')')
        return maxid
    
    # 当該キーワードに新規投稿があるか確認
    newest_id = get_newestid(data)
    if(newest_id <= maxid):
        # 新規投稿なし
        return maxid
    maxid = newest_id
    
    # 検索結果を解析
    notify_cnt = check_data(data, current_id, keystr)
    print(keystr + ': ' + str(notify_cnt) + '件通知しました。')

    return maxid

# メイン処理
http = urllib3.PoolManager()
current_id = get_maxid()
new_maxid = current_id
for k in settings.KEYWORDS:
    for sub in settings.SUB_KEYWORDS:
        params = {
            'query' : k + ' ' + sub,
            'tweet.fields' : 'created_at',
        }
        
        id = get_tweet(http, params, current_id)
        
        if(Decimal(id) > Decimal(new_maxid)):
            new_maxid = id

update_maxid(new_maxid)
