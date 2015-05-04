import datetime

from scraper import TASMusicScraper, SOMAFMMusicScraper
from rdio_playlist_creator import TrackListCreator, RdioAuthenticator, PlaylistPopulator
from spotify_playlist_creator import SpotifyPlaylistCreator
from page_structures import TAS_PAGE, SOMA_FM_BAGEL_PAGE

def TAS_playlist_maker():

    my_scraper = TASMusicScraper(TAS_PAGE['url'])
    playlist_maker('TAS Top 20', my_scraper, TAS_PAGE, 'The top 20 songs per week played on The Alternate Side WFUV 903')

def BAGEL_FM_playlist_maker():
    my_scraper = SOMAFMMusicScraper(SOMA_FM_BAGEL_PAGE['url'])
    playlist_maker('BAGEL FM top 30 tracks', my_scraper, SOMA_FM_BAGEL_PAGE, 'The top 30 tracks by spin played on Bagel FM')

def playlist_maker(playlist_name, scraper, playlist_page, playlist_description):

    soup_page = scraper.get_soup_page()
    find_result = scraper.get_page_items(playlist_page['layout'],soup_page)


    if find_result:
        playlist_name_time = playlist_name + ' ' + datetime.date.today().strftime('%m-%d-%Y')
        playlist_user = input("Is this playlist for David or Jenny?: ").strip()

        if playlist_user.lower() == 'david':

            my_rdio_instance = RdioAuthenticator().set_rdio_instance()
            my_tracklist_creator = TrackListCreator(find_result)
            track_list = my_tracklist_creator.check_artist_and_set_track_list(my_rdio_instance)
            my_playlist_populator = PlaylistPopulator(playlist_name_time)
            playlist_key = my_playlist_populator.get_playlist_keys(my_rdio_instance)
            playlist_result = my_playlist_populator.create_or_update_playlist(my_rdio_instance, track_list, playlist_key,
                                                                  playlist_description)
            print('playlist created!')

        elif playlist_user.lower() == 'jenny':
            my_spotify_playlist_creator_instance = SpotifyPlaylistCreator(find_result)
            playlist_id = my_spotify_playlist_creator_instance.check_playlist('julessurm', playlist_name_time)
            track_list = my_spotify_playlist_creator_instance.check_artist_and_set_track_list()
            playlist_result = my_spotify_playlist_creator_instance.update_playlist('julessurm', playlist_id, track_list)

            print('playlist created!')
        else:
            print('invalid user!')
    else:
        print("We didn't get a result!")

if __name__ == '__main__':
    # TAS_playlist_maker()
    BAGEL_FM_playlist_maker()
