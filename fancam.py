from youtubesearchpython import VideosSearch

class Fancam():
    def __init__(self, idol_name):
        self.search_amount = 5
        self.yt_search = VideosSearch(idol_name + ' fancam', limit=self.search_amount)
        self.result = self.yt_search.result()
        self.video_output = {}
    
        self.run()

    def video_info(self):
        for search in range(self.search_amount):
            self.search_output = self.result.get('result')[search]
            self.video_title = self.search_output.get('title')
            self.video_URL = self.search_output.get('link')

            self.video_output.update({self.video_title : self.video_URL})
            
        return self.video_output

    def run(self):
        self.video_info()

fancam = Fancam('jisoo')

