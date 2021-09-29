def changePlaybackState(sp, deviceId):
    if sp.current_playback() == None:
        sp.transfer_playback(deviceId)
    else:
        if sp.current_playback()['is_playing'] == True:
            sp.pause_playback()
        else:
            sp.start_playback()

def changeTrack(sp, direction):
    if direction > 0:
        sp.next_track()
    else:
        sp.previous_track()

def changeVolume(sp, direction):
    if direction > 0:
        sp.volume(min(sp.current_playback()['device']['volume_percent']+direction, 100))
    else:
        sp.volume(max(sp.current_playback()['device']['volume_percent']+direction, 0))

def changeRepeatState(sp):
    if sp.current_playback()['repeat_state'] == "track":
        sp.repeat("context")
    else:
        sp.repeat("track")

def changeShuffleState(sp):
    if sp.current_playback()['shuffle_state'] == True:
        sp.shuffle(False)
    else:
        sp.shuffle(True)

def changeCurrentlyPlayedPlaylist(sp, currentlyChosen):
    sp.start_playback(context_uri = sp.current_user_playlists()['items'][currentlyChosen]['uri'])

def changeCurrentlyChosenPlaylist(sp, currentlyChosen, direction):
    currentlyChosen = (currentlyChosen + direction)%(len(sp.current_user_playlists()['items']))
    print(sp.current_user_playlists()['items'][currentlyChosen]['name'])
    return currentlyChosen

def addCurrentTrackToCurrentlyChosenPlaylist(sp, currentlyChosen):
    if sp.current_user_playlists()['items'][currentlyChosen]['owner']['uri'] != sp.current_user()['uri']:
        print("You are not the owner of the playlist you are trying add the song to")
        return
    allSongs = []
    for i in range(int(sp.current_user_playlists()['items'][currentlyChosen]['tracks']['total']/100)+1):
        allSongs += sp.playlist_tracks(sp.current_user_playlists()['items'][currentlyChosen]['uri'], limit=100, offset = i*100)["items"]
    uriAllSongs = [i["track"]["uri"] for i in allSongs]
    if sp.currently_playing()["item"]["uri"] in uriAllSongs:
        print("Already there")
    else:
        print("Added")
        sp.playlist_add_items(sp.current_user_playlists()['items'][currentlyChosen]['uri'], [sp.currently_playing()["item"]["uri"]])

def goBack15Seconds(sp):
    currentPlayback = sp.current_playback()
    sp.start_playback(context_uri= currentPlayback['context']['uri'], offset={"uri": sp.currently_playing()["item"]['uri']}, position_ms=max(0, currentPlayback["progress_ms"]-15000))
