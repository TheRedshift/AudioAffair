import sys
import pitchReader, processing, beats_per_minute2
import generated_vlc as vlc
import time
import math
from multiprocessing import Process
import lights

def playSong():

    instance = vlc.Instance()

    player = instance.media_player_new()

    player.audio_set_volume(50) # set to 1 for now because im getting bored of piano music

    media = instance.media_new(sys.argv[1])

    player.set_media(media)

    player.play()
    time.sleep(10)


def printArray():

    reader = pitchReader.pitchreader(sys.argv[1], sys.argv[2])

    format_window = processing.Format(8, 100)

    processor = processing.WaveProcess(44100, .01, format_window)

    for i in reader:

        myarray = processor.get_square()
        print '\n'.join([str(x) for x in myarray])
        #time.sleep(0.1)
        #print chr(27) + "[2J"
        print "\n"
        processor.update(i)

def rhythmManager(grid):
    bpm = get_file_bpm(sys.argv[1])
    controlLightArray(grid)

if __name__ == "__main__":
    x_channel_list = [3,5,7,8,10,11,12,13]
    y_channel_list = [15,16,18,22,26,19,21,23]
    lights.setupLEDs(x_channel_list, y_channel_list)

    grid = [[True,False,True,False,True,False,True,False]]*8

    grid2 = [[False,True,False,True,False,True,False,True]]*8
    #grid = [[True, False, True, True, False, True, False, True],[True, False, True, False, True, False, True, True],[True, False, False, True, True, True, True],[True,True,True, True, False, False, Fasle, False]]*2
    while(True):
	temp = math.floor(time.clock())
	temp = temp % 2
        if(temp == 0):
            lights.updateLEDs(grid, x_channel_list, y_channel_list)
        else:
            lights.updateLEDs(grid2, x_channel_list, y_channel_list)


    p1 = Process(target = playSong, args=())
    p2 = Process(target= printArray, args=())

    p1.start()
    p2.start()

    p1.join()
    p2.join()

