#Code created by Diego H. O. R. Antunes

#Details about:

# Before starting install TikTokApi using "pip install TikTokApi" and playwright using "python3 -m playwright install". Your system must have the dependencies installed "libicui18n.so.66 libicuuc.so.66 libwebp.so.6 libffi.so.7"

# Solution presented:
# Create a bot that enters the browser, enters the account you want to analyze and obtain the data by reading the content of the website.

# Current solution:
# Use tiktok api library to facilitate this - https://github.com/davidteather/TikTok-Api

#Importing tiktok library
from TikTokApi import TikTokApi
import os

#asking the user to enter the Username of the account you want to be analyzed in tiktok
account = str(input("Enter the Username of the account you want to be analyzed:"))

#asking the user to enter the amount of videos he wants to analyze from the last video released by the account
n = int(input("Enter the amount of videos you want to be analyzed from the last video posted:"))

#asking the user to enter the Proxie (It's needed because of captch) - https://github.com/davidteather/TikTok-Api/issues/397
# proxy = str(input("Proxie (It's needed because of captch) (Ex: 80.48.119.28:8080 ):"))

api = TikTokApi(custom_verify_fp=os.environ.get("verifyFp", None))

user_id = api.user(username=account).info().id
sec_uid = api.user(username=account).info().secUid
get_videos = api.user(user_id=user_id, sec_uid=sec_uid).videos(count=n)

#Defining a function with values ​​present in the TikTokApi request
def list_data(snapshot):
  listData = {}
  listData['user_name'] = snapshot['author']['uniqueId']
  listData['video_id'] = snapshot['id']
  listData['video_desc'] = snapshot['desc']
  listData['video_time'] = snapshot['createTime']
  listData['video_length'] = snapshot['video']['duration']
  listData['video_link'] = 'https://www.tiktok.com/@{}/video/{}?lang=en'.format(listData['user_name'], listData['video_id'])
  listData['n_likes'] = snapshot['stats']['diggCount']
  listData['n_shares'] = snapshot['stats']['shareCount']
  listData['n_comments'] = snapshot['stats']['commentCount']
  listData['n_plays'] = snapshot['stats']['playCount']
  return listData

#variable with details about the videos requested by the user
videos_data = [list_data(n) for n in get_videos]

#Creating a spreadsheet with the data obtained.
videos_data_ft = pd.DataFrame(videos_data)
videos_data_ft.to_csv('{}_data_videos.csv'.format(username),index=False)
