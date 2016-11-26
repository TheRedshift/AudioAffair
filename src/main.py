import sys
import pitchReader, processing

if __name__ == "__main__":

    reader = pitchReader.pitchreader(sys.argv[1], sys.argv[2])

    format_window = processing.Format(8, 100)

    processor = processing.WaveProcess(44100, .001, format_window)

    for i in reader:

        myarray = processor.get_square()
        print '\n'.join([str(x) for x in myarray])
        print "\n"

        processor.update(i)
