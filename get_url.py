# importing pafy
import pafy
import os
import csv

# url of playlist
url = "https://www.youtube.com/watch?v=eDUSn1M3dLM&list=PLQvvxnU2-Itfz2v8jeVJYybgyifBvJjZy"


class Playlist_Scraper():
    def __init__(self):
        self.url_list = {
            "01": "https://www.youtube.com/playlist?list=PL152bjytsMC4Goscddi5bS9xjHB_2mDUx",
        }

        # self.save_directory = os.path.join(os.getcwd(), 'Video')
        # if not os.path.exists(self.save_directory):
        #     os.makedirs(self.save_directory)

        self.csv_writer = csv.writer(open("playlist.csv", "w", encoding='utf-8', newline=''))

    def start_scraping(self):
        for season, url in self.url_list.items():
            self.get_playlist_urls(season, url)

    def get_playlist_urls(self, season, url):
        # getting playlist
        playlist = pafy.get_playlist(url)

        # getting playlist items
        items = playlist["items"]

        for item in items:
            # getting pafy object
            i_pafy = item['pafy']

            # getting watch url
            title = i_pafy.title
            videoid = i_pafy.videoid

            row = [season, url, title, videoid]

            self.csv_writer.writerow(row)
            print(row)


if __name__ == '__main__':
    app = Playlist_Scraper()
    app.start_scraping()
