import sys
import pitchReader, processing
import generated_vlc as vlc
import time
from multiprocessing import Process


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


if __name__ == "__main__":

    p1 = Process(target = playSong, args=())
    p2 = Process(target= printArray, args=())

    p1.start()
    p2.start()

    p1.join()
    p2.join()
