#!/usr/bin/env python3
# coding=utf-8

import dbus
import base64
import requests


def get_as_base64(url):
    # From https://stackoverflow.com/questions/38408253/way-to-convert-image-straight-from-url-to-base64-without-saving-as-a-file-in-pyt
    return base64.b64encode(requests.get(url).content)

session_bus = dbus.SessionBus()
try:
    player_obj = session_bus.get_object('org.mpris.MediaPlayer2.chrome', '/org/mpris/MediaPlayer2')
except dbus.exceptions.DBusException:
    print(':musical_note:')
else:
    player_control_interface = dbus.Interface(player_obj, dbus_interface='org.mpris.MediaPlayer2.Player')
    player_props_interface = dbus.Interface(player_obj, 'org.freedesktop.DBus.Properties')
    player_all_props = player_props_interface.GetAll('org.mpris.MediaPlayer2.Player')

    title = player_all_props[dbus.String('Metadata')][dbus.String('xesam:title')]
    status = player_all_props[dbus.String('PlaybackStatus')]
    art_url = player_all_props[dbus.String('Metadata')][dbus.String('mpris:artUrl')]

    if status == 'Playing':
        icon_name = 'media-playback-start'
    else:
        icon_name = 'media-playback-pause'

    print(f'{title} | iconName={icon_name} length=25')
    print('---')
    print(f'| image={get_as_base64(art_url).decode()} imageWidth=256')
    print('Next | iconName=media-skip-forward bash="qdbus org.mpris.MediaPlayer2.chrome /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next" terminal=false refresh=true')
    if status == 'Playing':
        print('Pause | iconName=media-playback-pause bash="qdbus org.mpris.MediaPlayer2.chrome /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause" terminal=false refresh=true')
    else:
        print('Play | iconName=media-playback-start bash="qdbus org.mpris.MediaPlayer2.chrome /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play" terminal=false refresh=true')
    print('Previous | iconName=media-skip-backward bash="qdbus org.mpris.MediaPlayer2.chrome /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous" terminal=false refresh=true')
    
