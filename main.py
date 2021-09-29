import spotipy
from system_hotkey import SystemHotkey
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import json
from allFunctions import *

global currentlyChosen, currentlyPlayed, deviceId
currentlyChosen = 0
currentlyPlayed = 0
deviceId = None

def funcionality(self, event, hotkey):
    global currentlyChosen, currentlyPlayed
    if event == ['control', 'shift', 'a']:
        changePlaybackState(sp, deviceId)
    elif event == ['control', 'shift', 'd']:
        changeTrack(sp, 1)
    elif event == ['control', 'shift', 's']:
        changeTrack(sp, -1)
    elif event == ['control', 'shift', 'q']:
        changeVolume(sp, -5)
    elif event == ['control', 'shift', 'w']:
        changeVolume(sp, 5)
    elif event == ['control', 'shift', 'e']:
        changeRepeatState(sp)
    elif event == ['control', 'shift', 'r']:
        changeShuffleState(sp)
    elif event == ['control', 'shift', 't']:
        changeCurrentlyPlayedPlaylist(sp, currentlyChosen)
    elif event == ['control', 'shift', 'f']:
        addCurrentTrackToCurrentlyChosenPlaylist(sp, currentlyChosen)
    elif event == ['control', 'shift', '1']:
        currentlyChosen = changeCurrentlyChosenPlaylist(sp, currentlyChosen, -1)
    elif event == ['control', 'shift', '2']:
        currentlyChosen = changeCurrentlyChosenPlaylist(sp, currentlyChosen, 1)
    elif event == ['control', 'shift', '3']:
        goBack15Seconds(sp)

hk = SystemHotkey(consumer=funcionality)
hk.register(('control', 'shift', 'a'), None)
hk.register(('control', 'shift', 's'), None)
hk.register(('control', 'shift', 'd'), None)
hk.register(('control', 'shift', 'f'), None)
hk.register(('control', 'shift', 'q'), None)
hk.register(('control', 'shift', 'w'), None)
hk.register(('control', 'shift', 'e'), None)
hk.register(('control', 'shift', 'r'), None)
hk.register(('control', 'shift', 't'), None)
hk.register(('control', 'shift', '1'), None)
hk.register(('control', 'shift', '2'), None)
hk.register(('control', 'shift', '3'), None)


scope = "user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative" 

with open("dataFile.json", "r") as readFile:
    data = json.load(readFile)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(data['id'], data['second'], 'http://example.com', scope=scope))

if sp.current_playback() == None:
    if 'deviceId' in data.keys():
        deviceId = data['deviceId']
    else:
        listOfDevices = sp.devices()['devices']
        print("Please, select your device:")
        for i in range(len(listOfDevices)):
            print("{} - {} {}".format(i, listOfDevices[i]['type'], listOfDevices[i]['name']))
        numbers = [str(i) for i in range(10)]
        while True:
            device = input()
            for i in device:
                if i not in numbers:
                    break
            else:
                deviceId = listOfDevices[int(device)]['id']
                data['deviceId'] = deviceId
                with open("dataFile.json", "w") as writeFile:
                    json.dump(data, writeFile)
                break
    try:
        changePlaybackState(sp, deviceId)
    except:
        print("Device is turned off.")
        exit(0)

print("Device is ready.")

while True:
    sleep(1)