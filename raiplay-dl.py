from __future__ import unicode_literals

import urllib.request
import subprocess
import argparse
import json
import os

from pathlib import Path

import youtube_dl

def get_raiplay_url(leaf):
  return 'https://www.raiplay.it/' + leaf

def convert_url_to_json(url):
  json_url = url.rstrip('/')
  if json_url.endswith(".html"):
    json_url = json_url.replace(".html", ".json")
  if not json_url.endswith(".json"):
    json_url = json_url + ".json"
  return json_url

def download(url, download_dir):
  print(f"Download directory set to {download_dir}")
  content_url = urllib.request.urlopen(convert_url_to_json(url))
  data = json.loads(content_url.read().decode())
  if 'video' in data:
    download_title(url, download_dir)
  elif 'items' in data:
    download_set(url, download_dir)
  elif 'blocks' in data:
    download_show(url, download_dir)

def download_show(url, download_dir):
  print(f"Downloading show @ {url}")
  content_url = urllib.request.urlopen(convert_url_to_json(url))
  data = json.loads(content_url.read().decode())
  for block in data['blocks']:
    if block['name'].strip() == 'Episodi' or block['name'].strip() == 'Puntate':
      for block_set in block['sets']:
        download_set(get_raiplay_url(block_set["path_id"]), download_dir)

def download_set(url, download_dir):
  print(f"Downloading set @ {url}")
  content_url = urllib.request.urlopen(convert_url_to_json(url))
  data = json.loads(content_url.read().decode())
  for episode in data['items']:
    download_title(get_raiplay_url(episode["path_id"]), download_dir)

def download_title(url, download_dir):
  print(f"Downloading title @ {url}")
  content_url = urllib.request.urlopen(convert_url_to_json(url))
  data = json.loads(content_url.read().decode())
  # print(json.dumps(data, indent=4))
  video_url = data['video']['content_url']
  video_title = data['episode_title'].replace('[^A-Za-z0-9\'àèéìòùÈ]+', '-') or data['name'].replace('[^A-Za-z0-9\'àèéìòùÈ]+', '-')
  import re
  data['name'] = re.sub('[^A-Za-z0-9\'àèéìòùÈ]+',' ', data['name'])

  video_filename = Path(f"{download_dir}/{data['name'].replace('[^A-Za-z0-9àèéìòùÈ]+', ' ').rstrip()}/{data['season'].replace('[^A-Za-z0-9àèéìòùÈ]+', ' ')}/{video_title.replace('[^A-Za-z0-9àèéìòùÈ]+', ' ')}.mp4")
  if (not video_filename.parent.is_dir()):
    os.makedirs(video_filename.parent)

  if os.path.isfile(video_filename):
    print(f"{video_filename} already downloaded, skipping...")
    return

  def rename_downloaded_file(d):
    if d['status'] == 'finished':
      os.rename(os.path.abspath(d['filename']), video_filename)

  ydl_opts = {
    # 'simulate' : True,
    'progress_hooks': [rename_downloaded_file],
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog='raiplay-dl', description='Downloader for the Italian streaming platform RaiPlay')
  parser.add_argument("url", help="URL of the content to download")
  parser.add_argument("-d", help="Directory to download content to", default="downloads", metavar='download_directory', dest='download_directory')
  args = parser.parse_args()
  download(args.url, args.download_directory)
