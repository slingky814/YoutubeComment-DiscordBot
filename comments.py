from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import urllib.parse as p
import re
import os
import pickle
import random

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(api_service_name, api_version, credentials=creds)

# authenticate to YouTube API
youtube = youtube_authenticate()

def get_video_id_by_url(url):
    """
    Return the Video ID from the video `url`
    """
    # split URL parts
    parsed_url = p.urlparse(url)
    # get the video ID by parsing the query of the URL
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise Exception(f"Wasn't able to parse video URL: {url}")

def get_comments(youtube, **kwargs):
    return youtube.commentThreads().list(
        part="snippet",
        **kwargs
    ).execute()

def get_comment(url):
    # URL can be a channel or a video, to extract comments
    #url = "https://www.youtube.com/watch?v=EwBA1fOQ96c"
    if "watch" in url:
        # that's a video
        video_id = get_video_id_by_url(url)
        params = {
            'videoId': video_id,
            'maxResults': 50,
            'order': 'relevance', # default is 'time' (newest)
        }
    else:
        # should be a channel
        channel_id = get_channel_id_by_url(url)
        params = {
            'allThreadsRelatedToChannelId': channel_id,
            'maxResults': 2,
            'order': 'relevance', # default is 'time' (newest)
        }
    # get the first 2 pages (2 API requests)
    n_pages = 2
    commentList = []
    for i in range(n_pages):

        # make API call to get all comments from the channel (including posts & videos)
        response = get_comments(youtube, **params)
        items = response.get("items")
        # if items is empty, breakout of the loop
        if not items:
            break
        for item in items:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            commentList.append(comment)

        if "nextPageToken" in response:
            # if there is a next page
            # add next page token to the params we pass to the function
            params["pageToken"] =  response["nextPageToken"]
        else:
            # must be end of comments!!!!
            break
    comment = commentList[random.randint(0, len(commentList)-1)]
    return comment
