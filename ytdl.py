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
    for url in urls:
        print("Attempting to grap: {0}".format(url))
        download(url)


def download(url):
    """Download a single video

    Arguments:
        url - A single URL to download

    returns:
        None
    """
    if not url.startswith("http://"):
        return

    yt = YouTube()
    yt.url = url

    try:
        video = select_video(yt)
        _download(url, video)
    except ValueError as e:
        print("Failed to retrieve video: {0} - {1}".format(url, e))
    except HTTPError as e:
        print("Oops! Youtube said NO!: {0} - {1}".format(url, e))


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


def _download(url, video):
    """Download the video from YouTube

    Arguments:
        url - The url of the video, for refrence only
        video - the pytube.video you want to download

    Raises:
        HTTPError - Ushualy if your request was blocked

    Returns:
        None
    """
    print("Downloading {1}: {0}".format(video, url))
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

