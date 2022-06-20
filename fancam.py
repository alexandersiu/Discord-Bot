from youtubesearchpython import VideosSearch

def get_Fancam(idol_Name):
    yt_Search = idol_Name + ' fancam'

    search_Amount = 10
    videos_Search = VideosSearch(yt_Search, limit=search_Amount)
    result = videos_Search.result()

    video_Dict = {}
    for i in range(search_Amount):
        video_Info = result.get('result')[i]
        video_URL = video_Info.get('link')
        video_Title = video_Info.get('title')
        video_Views = video_Info.get('viewCount')
        video_Views = list(video_Views.values())[0]
        video_Views = video_Views.split(' ')[0]
        video_Views = int(video_Views.replace(',', ''))
        video_Dict.update({video_URL : video_Views})

    sorted_Dict = dict(sorted(video_Dict.items(), key=lambda item: item[1], reverse=True))
    return sorted_Dict