"""
Python script to populate a playlist to sync down to a device.
The playlist contains the first episode of each show in the TV section.
Shows specified in ExludeShows are not added to the playlist.
"""
from plexapi.server import PlexServer
#from plexapi.myplex import MyPlexAccount
import ConfigParser

# plex = PlexServer()


baseurl = 'http://192.168.2.50:32400'
token = 'zbv7hDnHEV2aGKRmQsRd'
plex = PlexServer(baseurl, token)
Config = ConfigParser.ConfigParser()
playlistName = ''

Config.read('CreateSyncList.cfg')

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

playlistName = ConfigSectionMap('General')['playlistname']
numberOfShows2Add = ConfigSectionMap('General')['numberofepisodes2sync']

startAfterThisShow = ConfigSectionMap(playlistName)['lastsyncedshow']

if playlistName == '':
    print ("No playlist specified. Please add PlaylistName under [General] in CreateSyncList.cfg")
    exit()


Playlist = plex.playlist(playlistName)

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
# Save the first items show for later usage
showName = ''
StartFromCurrent = False
StartAfterLast = False

# Check for the last show in the playlist and start adding episodes after that.
# We don't want to  transcode and sync those again
for episode in Playlist.items():
    showName = episode.grandparentTitle
    StartFromCurrent = True
    TVEpisodes += 1
#    Playlist.removeItem(episode)

# answer = input("Sync the device to clear all episodes! Press enter when ready.")

# If we still have shows left in the current playlist, start from that show
if(showName != ''):
    firstShowToAdd = showName
    StartAfterLast = True

BreakOnNext = False

TVsection = plex.library.section('TV')
for shows in TVsection.all():
    # print(shows.title)
    if(StartFromCurrent):
        if(firstShowToAdd != shows.title):
            continue
        else:
            StartFromCurrent = False
            continue    # Start adding next show

    if ExcludeShows.count(shows.title) != 0:
        print('Excluded: ', shows.title)
        continue


#    if(StartAfterLast):
#        if(startAfterThisShow != shows.title):
#            continue
#        else:
#            StartAfterLast = False

    if(len(shows.episodes()) <= 3):
        for episode in shows.episodes():
            thefirstlist.append(episode)
            TVEpisodes += 1
        AllEpisodes.append(shows.title)
    else:
        thefirstlist.append(shows.episodes()[0])

    TVEpisodes += 1;

    if(TVEpisodes >= int(numberOfShows2Add)):
        break


Playlist.addItems(thefirstlist)

Config.set(playlistName, 'FirstSyncedShow', thefirstlist[0].grandparentTitle)
Config.set(playlistName, 'LastSyncedShow', shows.title)

with open(r'CreateSyncList.cfg', 'wb') as configfile:
    Config.write(configfile)

print('Episodes added to the Playlist:', TVEpisodes)
for show in AllEpisodes:
    print( 'All episodes are added for show: ', show)