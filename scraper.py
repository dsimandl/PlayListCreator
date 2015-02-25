from urllib import request
from bs4 import BeautifulSoup

url = "http://thealternateside.org/"
page = request.urlopen("http://thealternateside.org/")
soup_altside = BeautifulSoup(page)
page.close()


top_albums_view = soup_altside.find("div", class_="view-top-albums")
top_songs = top_albums_view.find("div", class_="field-content")
top_song_list = top_songs.find_all("p")

for top_song in top_song_list:
    print(list(top_song)[1])
    print(list(top_song)[3])