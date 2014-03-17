#!/bin/env python2
import argparse
from sys import argv
from pytube import YouTube
from urllib2 import HTTPError 

def _real_main(urls):
    """Download the youtube videos provided

    Arguments:
        urls - A iterable list of hyperlinks to the desired videos

    Returns: 
        None
    """
    _yt = YouTube()

    for url in urls:
        print("Attempting to grap: {0}".format(url))
        if not url.startswith("http://"): 
            continue

        url = url.rstrip()
        _yt.url = url

        try:
            _video = select_video(_yt)
            download(url, _video)

        except ValueError as e:
            print("Failed to download: {0}: {1}".format(url, e))

        except HTTPError as e:
            print("OOPS! Youtube said no: {0}: {1}".format(url, e))


def select_video(yt, prefered_codec=['mp4','flv']):
    """Find the best codec for your requested video

    Arguments:
        yt - The YouTube object refrencing the video
        prefered_codec - A list of preffered codecs

    Raises:
        ValueError - if the codec is not found

    Returns:
        A refrence to the video that best matched your request.
    """
    for codec in prefered_codec:
        video_options = yt.filter(codec)
        if video_options and len(video_options) > 0:
            return sorted(video_options, key=lambda v: v.resolution).pop()
    raise ValueError("No Codec Found")


def download(url, video, quiet=False):
    """Download the video from YouTube

    Arguments:
        url - The url of the video, for refrence only
        video - the pytube.video you want to download
        quiet - If true, disables verbose output.

    Raises:
        HTTPError - Ushualy if your request was blocked

    Returns:
        None
    """
    def _show_progress(current, total):
        print("{0}: {1}/{2}".format(url, current, total))

    if not quiet:
        print("Downloading {1}: {0}".format(video, url))
        video.on_progress = _show_progress

    video.download()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-infile", type=argparse.FileType("r"), help="Read URLS from a file. ('-' for STDIN)")
    parser.add_argument("URL", nargs="*", help="A space delimited list of YouTube URLs")
    args = parser.parse_args(argv[1:])
    
    if args.infile:
        _urls = args.infile
    else:
        _urls = args.URL

    _real_main(_urls)

