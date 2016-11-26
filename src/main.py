import sys
import pitchReader#processing

if __name__ == "__main__":

    reader = pitchReader.pitchreader(sys.argv[1], sys.argv[2])

    for i in reader:
        print i
