# coding: UTF-8
import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
#
# 指定されたTwitterのユーザー名のTweetを収集するクラス
#　- collectTweet でインスタンスにTweetデータを保持
# - writeCSV で保持したTweetデータをCSVファイルとして保存
#
class TweetCollector:
    #Twitterの取得URL
    __TWITTER_URL = (
        "https://twitter.com/i/profiles/show/"
        "%(user_name)s/timeline/tweets?include_available_features=1&include_entities=1"
        "%(max_position)s&reset_error_state=false"
    )

    __user_name = ""    #取得するTwitterのユーザー名
    __tweet_data = []   #Tweetのブロックごと配列

    #
    # コンストラクタ
    #
    def __init__(self, user_name):
        self.__user_name = user_name

        #項目名の設定
        row = [
            "ツイートID",
            "名前",
            "ユーザー名",
            "投稿日",
            "本文",
            "返信数",
            "リツイート数",
            "いいね数"
        ]
        self.__tweet_data.append(row)

    #
    # Tweetの収集を開始する
    #
    def collectTweet(self):
        self.nextTweet(0)

    #
    # 指定されたポジションを元に次のTweetを収集する
    #
    def nextTweet(self, max_position):
        # max_position に 0 が指定されていたらポジション送信値なし
        if max_position == 0:
            param_position = ""
        else:
            param_position = "&max_position=" + max_position

        # 指定パラメータをTwitterのURLに入れる
        url = self.__TWITTER_URL % {
            'user_name': self.__user_name,
            'max_position': param_position
        }

        # HTMLをスクレイピングして、Tweetを配列として格納
        res = requests.get(url)
        soup = BeautifulSoup(res.json()["items_html"], "html.parser")

        items = soup.select(".js-stream-item")

        for item in items:
            row = []
            row.append(item.get("data-item-id")) #ツイートID
            row.append(item.select_one(".fullname").get_text().encode("cp932", "ignore").decode("cp932")) #名前
            row.append(item.select_one(".username").get_text()) #ユーザー名
            row.append(item.select_one("._timestamp").get_text()) #投稿日
            row.append(item.select_one(".js-tweet-text-container").get_text().strip().encode("cp932", "ignore").decode("cp932")) #本文
            row.append(item.select(".ProfileTweet-actionCountForPresentation")[0].get_text()) #返信カウント
            row.append(item.select(".ProfileTweet-actionCountForPresentation")[1].get_text()) #リツイートカウント
            row.append(item.select(".ProfileTweet-actionCountForPresentation")[3].get_text()) #いいねカウント

            self.__tweet_data.append(row)

        print(str(max_position) + "取得完了")
        #time.sleep(0.1) #負荷かけないように

        # ツイートがまだあれば再帰処理
        if res.json()["min_position"] is not None:
            self.nextTweet(res.json()["min_position"])

    def data2pandas(self):
        data = self.__tweet_data
        print(len(data))
        npdata= np.array(data)
        print(npdata)
        df = pd.DataFrame(npdata[1:,:], columns=['ID', 'name', 'user_name','submit_date','tweet','return_num','retweet_num','good_num'])
        print(df)
        df.to_pickle('pandas_obj.pkl')

def convert_to_datetime(date):
    try:
        return pd.to_datetime(date, format='%Y年%m月%d日')
    except:
        #print(date)
        today = datetime.date.today()
        y_m_d = str(today.year)+'年'+str(date)
        try:
            y_m_d = pd.to_datetime(y_m_d, format='%Y年%m月%d日')
            return pd.to_datetime(y_m_d, format='%Y-%m-%d')
        except:
            return pd.to_datetime(datetime.date.today(), format='%Y-%m-%d')


def return_year(date):
    return date.year
def return_month(date):
    return date.month

def return_year_month(date):
    return pd.to_datetime(str(date.year)+'-'+str(date.month), format='%Y-%m')

def str2int(data):
    try:
        return int(data)
    except:
        return int(data.replace(',',''))

###########################
def gettweetlog(username):#処理
##########################
    twc = TweetCollector(username) #Twitterのユーザー名を指定 "@bobtenshi"
    twc.collectTweet()
    twc.data2pandas()

    df = pd.read_pickle('pandas_obj.pkl')
    df['submit_date']=df['submit_date'].map(convert_to_datetime)
    print(df['submit_date'])
    df['year'] = df['submit_date'].map(return_year)
    df['month'] = df['submit_date'].map(return_month)
    df['year_month'] = df['submit_date'].map(return_year_month)
    #print(df['year'])
    #print(df.head())
    #print(df.dtypes)
    df.index = df['year_month']
    #rint(type(df.index))
    #print(df['retwet_num'])
    df=df[df['user_name'] == '@bobtenshi']
    #print(df.head())
    df_n=df[['good_num','retweet_num']]
    df_n['tweet_num'] = 1


    df_n.loc[df['good_num'] == '', 'good_num'] = '0'
    df_n.loc[df['retweet_num'] == '', 'retweet_num'] = '0'
    df_n['good_num'] = df_n['good_num'].map(str2int)
    df_n['retweet_num'] = df_n['retweet_num'].map(str2int)

    print(df_n['good_num'][1])
    a=df_n['good_num'][1]

    print(df_n['good_num'].all)
    print(df_n.info())

    df_y = df_n.set_index([df_n.index.year, df_n.index.month,df_n.index])
    df_y.index.names = ['year','month','date']
    print(df_y.head())
    print(df_y.dtypes)
    print(df_y.sum(level=['year','month']))

    plt.figure(figsize=(10, 10), dpi=50)
    df_y.sum(level=['year','month']).plot()
    plt.savefig('./document/image/graph.png')
    plt.close('all')
    print('fin')