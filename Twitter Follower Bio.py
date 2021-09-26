#export follower data of an account

import tweepy
import pandas as pd

def lookup_user_list(user_id_list, api):
    full_users = []
    users_count = len(user_id_list)
    try:
        for i in range((users_count // 100) + 1):
            print (i)
            full_users.extend(api.lookup_users(user_ids=user_id_list[i * 100:min((i + 1) * 100, users_count)]))
        return full_users
    except tweepy.TweepError:
        print ('Something went wrong, quitting...')

consumer_key = 'XXXXXXXX'
consumer_secret = 'XXXXXXX'
access_token = 'XXXXXX'
access_token_secret = 'XXXXXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

ids = []
for page in tweepy.Cursor(api.followers_ids, screen_name="XXXXX").pages():
    ids.extend(page)

#sub in screen name of account you want to get follower IDs from

results = lookup_user_list(ids, api)
all_users = [{'id': user.id,
             'Name': user.name,
             'Statuses Count': user.statuses_count,
             'Friends Count': user.friends_count,
             'Screen Name': user.screen_name,
             'Followers Count': user.followers_count,
             'Location': user.location,
             'Language': user.lang,
             'Created at': user.created_at,
             'Time zone': user.time_zone,
             'Geo enable': user.geo_enabled,
             'Description': user.description}
             for user in results]

df = pd.DataFrame(all_users)

df.to_csv('All followers.csv', index=False, encoding='utf-8')
