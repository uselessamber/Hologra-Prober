import requests
import re
import random
import tqdm
import time
from pytube import *
from art import *

URL = "https://www.youtube.com/playlist?list=PL1NeGg1woXqngQytLzL8lJJLYwmzk1Wuq"
html = requests.get(URL).text
info = re.findall('(?<={"label":").*?(?="})', html)
hologra_links = []

class HolograEpisode:
    def __init__(self, url):
        temp = YouTube(url)
        self.url = url
        self.posted_date = time.mktime(temp.publish_date.timetuple())

def load_Hologra():
    urls = []
    print("loading Hologra into database: ")
    playlist = Playlist(URL)
    for link in tqdm.tqdm(playlist):
        urls.append(HolograEpisode(link))
    return urls


def update():
    new_playlist = Playlist(URL).video_urls
    if len(new_playlist) > len(hologra_links):
        print("Found new episode: ")
        print("Episode Matching...")
        for episode in tqdm.tqdm(hologra_links):
            try:
                new_playlist.remove(episode.url)
            except:
                print("Minor Error, not a big issue")
        output = []
        print("Write new episode into database...")
        for new_episode in tqdm.tqdm(new_playlist):
            hologra_links.append(HolograEpisode(new_episode))
            output.append(HolograEpisode(new_episode))
        print("Return new episode:")
        return output
    print("Found no new episode")
    return None

def get_latest_Hologra():
    latest_hologra = None
    for hologra in hologra_links:
        if latest_hologra == None:
            latest_hologra = hologra
        else:
            if latest_hologra.posted_date < hologra.posted_date:
                latest_hologra = hologra
    return latest_hologra

def get_random_Hologra():
    return random.choice(hologra_links)

def init():
    global hologra_links
    hologra_links = load_Hologra()
