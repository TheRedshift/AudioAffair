import sys
import pitchReader, processing
import generated_vlc as vlc
import time

instance = vlc.Instance()

player = instance.media_player_new()

player.audio_set_volume(1) # set to 1 for now because im getting bored of piano music

media = instance.media_new('test.wav')

player.set_media(media)

player.play()
time.sleep(1)