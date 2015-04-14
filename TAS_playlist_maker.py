from scraper import MusicScraper
from rdio_playlist_creator import TrackListCreator, RdioAuthenticator, PlaylistPopulator
from spotify_playlist_creator import SpotifyPlaylistCreator



my_scraper = MusicScraper('http://thealternateside.org/')
soup_page = my_scraper.get_soup_page()
find_result = my_scraper.get_page_items([('find', ('div', 'view-top-albums')),
                                                               ('find', ('div', 'field-content')), ('find_all', 'p')],
                                        soup_page)

playlist_user = input("Is this playlist for David or Jenny?: ").strip()

if playlist_user.lower() == 'david':
    if find_result:
        my_rdio_instance = RdioAuthenticator().set_rdio_instance()
        my_tracklist_creator = TrackListCreator(find_result)
        track_list = my_tracklist_creator.check_artist_and_set_track_list(my_rdio_instance)
        my_playlist_populator = PlaylistPopulator('TAS Top 20')
        playlist_key = my_playlist_populator.get_playlist_keys(my_rdio_instance)
        playlist_result = my_playlist_populator.create_or_update_playlist(my_rdio_instance, track_list, playlist_key,
                                                                  'The top 20 songs per week played on The Alternate Side WFUV 903')
        print(playlist_result)
    else:
        print('There was an error!')
elif playlist_user.lower() == 'jenny':
    if find_result:
        my_spotify_playlist_creator_instance = SpotifyPlaylistCreator(find_result)
        my_playlist_id = my_spotify_playlist_creator_instance.check_playlist('julessurm')
        print(my_playlist_id)
else:
    print('invalid user!')
