# Python YouTube API
# https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/

import json

api_key = 'AIzaSyB5bH0RkyiWwZTGN6HW4S-GwlfUTR94Co'


from googleapiclient.discovery import build

youtube = build('youtube','v3',developerKey=api_key)

request = youtube.channels().list(
    part='contentDetails, statistics',
    forUsername='schafer5'
)
response = request.execute()
# print(response)


# Get channel details

pl_request = youtube.playlists().list(
    part = 'contentDetails, snippet',
    channelId='UCCezIgC97PvUuR4_gbFUs5g'
)

pl_response = pl_request.execute()
# print(pl_response)

playlist_data = pl_response
print(json.dumps(playlist_data,indent=4,sort_keys=True,default=str))
