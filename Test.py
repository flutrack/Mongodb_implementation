__author__ = 'gsvic'

from PyFlutrack.DataStreamer import FluTrackStreamer

def main():
    streamer = FluTrackStreamer()
    streamer.StreamData()

if __name__ == "__main__":
    main()