#Code created by Diego H. O. R. Antunes

#Details about:

# Before starting install TikTokApi using "pip install TikTokApi", pandas using "pip install pandas" and playwright using "python3 -m playwright install". Your system must have the dependencies installed "libicui18n.so.66 libicuuc.so.66 libwebp.so.6 libffi.so.7"

# Solution presented:
# Create a bot that enters the browser, enters the account you want to analyze and obtain the data by reading the content of the website.

# Current solution:
# Use tiktok api library to facilitate this - https://github.com/davidteather/TikTok-Api

#Importing tiktok library
from TikTokApi import TikTokApi
import os
import pandas as pd


url = str(input("Video URL:"))


# for i in data['urls']:
#     print(i)

def video_info(url):
    with TikTokApi(custom_verify_fp=os.environ.get("verifyFp", None)) as api:
        video = api.video(url=url)
        return video.id


def video_data(video_id):
    with TikTokApi(custom_verify_fp=os.environ.get("verifyFp", None)) as api:
        video = api.video(id=video_id)
        data = video.info()
        return data

def simple_dict(tiktok_dict):
  to_return = {}
  to_return['user_name'] = tiktok_dict['author']['uniqueId']
  to_return['user_id'] = tiktok_dict['author']['id']
  to_return['video_id'] = tiktok_dict['id']
  to_return['video_desc'] = tiktok_dict['desc']
  to_return['video_time'] = tiktok_dict['createTime']
  to_return['video_length'] = tiktok_dict['video']['duration']
  to_return['video_link'] = 'https://www.tiktok.com/@{}/video/{}?lang=en'.format(to_return['user_name'], to_return['video_id'])
  to_return['n_likes'] = tiktok_dict['stats']['diggCount']
  to_return['n_shares'] = tiktok_dict['stats']['shareCount']
  to_return['n_comments'] = tiktok_dict['stats']['commentCount']
  return to_return

link_data = simple_dict(video_data(video_info(url)))
print(link_data)
user_videos_df = pd.DataFrame(link_data, index=[0])
user_videos_df.to_csv('{}_videos.csv'.format(link_data['user_name']),index=False)
