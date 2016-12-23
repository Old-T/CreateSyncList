"""
Python script to populate a playlist to sync down to a device.
The playlist contains the first episode of each show in the TV section.
Shows specified in ExludeShows are not added to the playlist.
"""
from plexapi.server import PlexServer
# plex = PlexServer()

from plexapi.myplex import MyPlexAccount

baseurl = 'http://192.168.2.50:32400'
token = 'zbv7hDnHEV2aGKRmQsRd'
plex = PlexServer(baseurl, token)

Playlist = plex.playlist('To Sync')

thefirstlist = [];
AllEpisodes = [];
TVEpisodes = 0;

# Define the Shows to exclude from the sync list
ExcludeShows = ['24', 'Agatha Raisin', 'The Americans', 'Arne Dahl', 'Better Call Saul', 'The Big Bang Theory',
                'The Blacklist', 'The Blacklist: Redemption',
                'Blackadder', 'Castle (2009)', 'Blindspot', 'Bones', 'Bosch', 'Broadchurch', 'Criminal Minds',
                'Criminal Minds: Beyond Borders',
                'Death in Paradise', 'Elementary', 'Fortitude', 'Friends', 'Game of Thrones', 'The Goose Mother',
                'Hawaii Five-0', 'Homeland',
                'Hooten & the Lady', 'House of Cards (US)', 'How I Met Your Mother', 'The Last Man on Earth',
                'Lethal Weapon', 'Lucifer',
                'Making a Murderer', 'Mars (2016)', 'MasterChef', 'MasterChef (US)', 'MasterChef Australia',
                'MasterChef Canada', 'MasterChef South Africa',
                'MasterChef: The Professionals', 'Midnight Sun', 'NCIS', 'NCIS: Los Angeles', 'NCIS: New Orleans',
                'Orange Is the New Black', 'Orphan Black',
                'Scorpion', 'Scrubs', 'Sherlock', 'Suits', 'The Taste', 'The Taste UK', 'Top Chef', 'Westworld'];

# First, clear the current laylist
for episode in Playlist.items():
    Playlist.removeItem(episode)

TVsection = plex.library.section('TV')
for shows in TVsection.all():
    # print(shows.title)
    if ExcludeShows.count(shows.title) != 0:
        print('Excluded: ', shows.title)
        continue

    if(len(shows.episodes()) <= 3):
        for episode in shows.episodes():
            thefirstlist.append(episode)
        AllEpisodes.append(shows.title)
    else:
        thefirstlist.append(shows.episodes()[0])

    TVEpisodes += 1;

Playlist.addItems(thefirstlist)

print('Episodes added to the Playlist:', TVEpisodes)
for show in AllEpisodes:
    print( 'All episodes are added for show: ', show)