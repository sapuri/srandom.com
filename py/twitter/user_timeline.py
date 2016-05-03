from twitter import *

CONSUMER_KEY = 'Pwyx6QZgunJsbrArLub7pNKwu'
CONSUMER_SECRET = 'D7J4xAE7aXLrqGyaKy8adpxtU1rrAEuZy8MaRUw3GUUzG6BLeO'

def user_timeline(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET, count):
    '''
    指定したユーザーのタイムラインを取得
    @param string oauth_token ユーザー
    @param string oauth_secret ユーザー
    @param string CONSUMER_KEY アプリ
    @param string CONSUMER_SECRET アプリ
    @param int count ツイート取得件数
    @return list timeline タイムライン
    '''
    # Twitterクラスを作成
    twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

    # タイムラインを取得
    timeline = twitter.statuses.user_timeline(count=count)

    return timeline

if __name__ == "__main__":
    oauth_token = ''
    oauth_secret = ''

    # 取得件数を指定 (最大200件)
    count = 200

    # 指定したユーザーのタイムラインを取得
    timeline = user_timeline(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET, count)

    for tweet in timeline:
        print ("{0} ({1})" .format(tweet['text'], tweet['created_at']))
        print ()
