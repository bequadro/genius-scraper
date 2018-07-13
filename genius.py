import sys
import os
import re
import pathlib
import eyed3
import requests
from bs4 import BeautifulSoup
import lyricsgenius as genius

def scrape_song_lyrics_from_url(title, artist):
	_title = re.sub('\W+', ' ', title).strip()
	_artist = re.sub('\W+', ' ', artist).strip()
	_location = _artist + ' ' + _title
	url = 'https://genius.com/' + _location.replace(' ', '-') + '-lyrics';
	print(url)
	try:
		page = requests.get(url)
		html = BeautifulSoup(page.text, "html.parser")
		lyrics = html.find("div", class_="lyrics").get_text()
		print('Success.')
		return lyrics.strip('\n')
	except:
		print('Not found.')
		return 0

if __name__ == "__main__":

	path = sys.argv[1]
	try:
		artist = sys.argv[2]
	except:
		artist = 0

	print('\nGENIUS SCRAPER')

	with open(os.path.join(os.path.dirname(__file__), 'api.key'), 'r') as f:
		api_key = f.read()
		print(api_key + '\n')
	f.close()

	api = genius.Genius(api_key)

	for mp3_file in pathlib.Path(path).glob('**/*.mp3'):
		tag = eyed3.load(mp3_file).tag
		title = tag.title
		if not artist:
			artist = tag.artist.split(',')[0]
		song = api.search_song(title, artist)
		if song:
			lyrics = song.lyrics
		else:
			lyrics = scrape_song_lyrics_from_url(title, artist)
		if lyrics:
			tag.lyrics.set(lyrics)
		tag.save(version=eyed3.id3.ID3_V2_4)
		print('')
