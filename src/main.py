import sys
import pitchReader, processing, beats_per_minute2
import generated_vlc as vlc
import time
import math
from multiprocessing import Process
#import lights


x_channel_list = [3,5,7,8,10,11,12,13]
y_channel_list = [15,16,24,22,26,19,21,23]

def playSong():

    instance = vlc.Instance()

    player = instance.media_player_new()

    player.audio_set_volume(50) # set to 1 for now because im getting bored of piano music

    media = instance.media_new(sys.argv[1])

    player.set_media(media)

    player.play()
    #time.sleep(10)


def printArray():

    reader = pitchReader.pitchreader(sys.argv[1], sys.argv[2])

    format_window = processing.FormatLine(5, 70)

    processor = processing.WaveProcess(44100, .01, format_window)

    for i in reader:

        myarray = processor.get_square()
        #lights.updateLEDs(myarray, x_channel_list, y_channel_list)
        print '\n'.join([str(r) for r in myarray])
        time.sleep(1)
        print chr(27) + "[2J"
        print "\n"
        processor.update(i)

#def rhythmManager(grid):
#    bpm = get_file_bpm(sys.argv[1])
#    controlLightArray(grid)

if __name__ == "__main__":
    #lights.setupLEDs(x_channel_list, y_channel_list)

    p1 = Process(target = playSong, args=())
    p2 = Process(target= printArray, args=())

    p1.start()
    p2.start()

    p1.join()
    p2.join()

