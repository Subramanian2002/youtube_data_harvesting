from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
from isodate import parse_duration
api_key = 'AIzaSyCTdyerIeb0_fOrlQeCZ2VNB29fqQ2x3Mc'
youtube = build('youtube', 'v3', developerKey=api_key)


def channel_info(channel_ids):
    channels = []
    request = youtube.channels().list(part='snippet,statistics,contentDetails',id = channel_ids)
    response = request.execute()
    data = dict(
          Channel_Name = response['items'][0]['snippet']['title'],
          Channel_Id = response['items'][0]['id'],
          Channel_Description = response['items'][0]['snippet']['description'],
          Channel_Views = response['items'][0]['statistics']['viewCount'],
          Subscription_Count = response['items'][0]['statistics']['subscriberCount'] ,
          Playlist_Id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
          Playlist_Name = response['items'][0]['snippet']['title'])
    channels.append(data)
    return channels  

def playlist(channel_id):
    playlists = []
    next_page_token = None
    while True:
        request = youtube.playlists().list(
            part='snippet,contentDetails', 
            channelId= channel_id ,
            maxResults=50,
            pageToken = next_page_token
            )
        response = request.execute()
            #print(response)
        for playlist in response.get('items',[]):
            data = dict(
                channel_id = playlist['snippet']['channelId'],
                playlist_id = playlist['id'],
                playlist_name = playlist['snippet']['title']
                )
            playlists.append(data)
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
            
    return playlists


from pprint import pprint
def video_info(channel_id):
    request = youtube.channels().list(id = channel_id,
                                   part = 'contentDetails')
    response = request.execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    #pprint(playlist_id)
    videos_details = []
    videos_id = []
    next_page_token = None
    
    while True:
        video_id_request = youtube.playlistItems().list(playlistId = playlist_id,
                                              part = 'snippet',
                                              maxResults = 50,
                                              pageToken = next_page_token)
        video_id_response = video_id_request.execute()
        for item in video_id_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            
            
            video_request = youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id)
            video_response = video_request.execute()
            view_count= int(video_response['items'][0]['statistics']['viewCount'])
            like_count = int(video_response['items'][0]['statistics']['likeCount'])
            if 'commentCount' in video_response['items'][0]['statistics']:
                 comment_count = int(video_response['items'][0]['statistics']['commentCount'])
            else:
                comment_count = 0
            
            data = dict(video_id =  video_response['items'][0]['id'],
                        channel_id =video_response['items'][0]['snippet']['channelId'],
                        video_name = video_response['items'][0]['snippet']['title'],
                        video_description = video_response['items'][0]['snippet']['description'],
                        #video_tags = video_response['items'][0]['snippet']['tags'],
                        video_duration = int(parse_duration(video_response['items'][0]['contentDetails']['duration']).total_seconds()),
                        publishedat = datetime.strptime(video_response['items'][0]['snippet']['publishedAt'],"%Y-%m-%dT%H:%M:%SZ"),
                        view_count= int(video_response['items'][0]['statistics']['viewCount']),
                        like_count = int(video_response['items'][0]['statistics']['likeCount']),
                        dislike_count = (view_count)-(like_count),
                        favorite_count = int(video_response['items'][0]['statistics']['favoriteCount']),
                        comment_count = comment_count,
                        thumbnail = video_response['items'][0]['snippet']['thumbnails']['default']['url'],
                        caption = video_response['items'][0]['contentDetails']['caption']
                       )
            videos_details.append(data)
        next_page_token = video_id_response.get('nextPageToken')
        if next_page_token is None:
            break
            
    return videos_details


def comment_info(ids):
    comments = []
    for i in ids:
        try:
            
            comments_request = youtube.commentThreads().list(
                        part='snippet',
                        videoId=i,
                        textFormat='plainText',
                        maxResults=50)
            comments_response = comments_request.execute()
            for item in comments_response['items']:
                data = dict(comment_id = item['id'],
                            video_id = item['snippet']['videoId'],
                            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay'],
                            comment_author = item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            comment_publishedat =item['snippet']['topLevelComment']['snippet']['publishedAt'])
                comments.append(data) 
        except:
            pass
              
    
    return comments



def main(channel_id):
    channel = channel_info(channel_id)
    playlists = playlist(channel_id)
    videos = video_info(channel_id)
    v_ids = []
    
    for item in videos:
        v_ids.append(item['video_id'])
    comment_details = comment_info(v_ids)
    data = {
        'channel_details': channel,
        'channel_playlists': playlists,
        'video_details': videos,
        'comment_details': comment_details
       }
    
    return data


            
        

    