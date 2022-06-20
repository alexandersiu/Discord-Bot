from youtubesearchpython import VideosSearch

def get_Fancam(idol_Name):
    yt_Search = idol_Name + ' fancam'

    videos_Search = VideosSearch(yt_Search, limit=1)
    result = videos_Search.result()

    video_Info = result.get('result')[0]
    video_URL = video_Info.get('link')
    video_Title = video_Info.get('title')
    video_Views = video_Info.get('viewCount')
    video_Views = list(video_Views.values())[0]

    return video_URL, video_Title, video_Views
