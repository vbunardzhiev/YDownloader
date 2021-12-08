import string
import os
import re
import argparse
import pafy
from pafy.util import xenc
from playlists_db import create_db, list_playlists, add_playlist, remove_playlist, get_playlist_url
from urllib.error import HTTPError

def song_downloaded(dir_, filename):
	extensions = ['ogg', 'm4a', 'webm']
	filename_ = filter_filename(filename)
	#print ('file: {}'.format(filename_))
	path = '{}\\{}'.format(dir_, filename_)
	for ext in extensions:
		if os.path.isfile('{}.{}'.format(path, ext)):
			return True
	return False

def make_string_printable(string_, trunc=None):
	for chars in string_:
		if chars not in string.printable:
			string_ = re.sub(re.escape(chars), '_', string_)
	if trunc:
		if len(string_) > 49:
			trunc = len(string_) - 49
			l = int((len(string_) - trunc - 3) / 2)
			return '{}..{}'.format(string_[:l+10], string_[-l+10:])
	return string_

def filter_filename(filename):
		ok = re.compile(r'[^\\/:*?"<>|]')
		seq_ = "".join(x if ok.match(x) else "_" for x in xenc(filename))
		return seq_

def list_playlists_from_db():
	for playlist in list_playlists():
		print (playlist)

def download_video(audio=True):
	pass

def sync_playlist(audio=True):
	pass

def sync_playlist(name, dir_):
	#print (name)
	url = get_playlist_url(name)
	#print (url)
	download_playlist(url, dir_)

def download_playlist(url, dir_):
	count = 0
	if not os.path.exists(dir_):
		os.makedirs(dir_)
	playlist = pafy.get_playlist2(url)
	playlist_len = playlist._len
	playlist_title = make_string_printable(playlist.title)
	print ('\nDloading playlist: [{}]'.format(playlist_title))
	for video in playlist:
		count += 1
		if song_downloaded(dir_, video.title):
			print ('Skipping: {}'.format(make_string_printable(video.title, trunc=46)).ljust(70) + '{}/{}'.format(count, playlist_len))
			continue
		try:
			bestaudio = video.getbestaudio()
		except OSError:
			continue # Different restrictions: age, country, deleted profile, etc. 
		filename = filter_filename(bestaudio.filename)
		filepath = '{}\\{}'.format(dir_, filename)
		print ('Dloading: {}'.format(make_string_printable(video.title, trunc=46)).ljust(70) + '{}/{}'.format(count, playlist_len))
		try:
			bestaudio.download(filepath=filepath)
		except HTTPError:
			continue

def usage():
	parser = argparse.ArgumentParser(usage='''ytsync <command> [-h] [<args>]''')
	parser._positionals.title = 'commands'

	subparsers = parser.add_subparsers(dest='command')

	parser_add = subparsers.add_parser('add', help='add playlist', usage='ytsync add <name> <url>')
	parser_add.add_argument('name', type=str, help='playlist name')
	parser_add.add_argument('url', type=str, help='playlist url')

	parser_remove = subparsers.add_parser('remove', help='remove playllist', usage='ytsync remove <name>')
	parser_remove.add_argument('name', type=str, help='name of the playlist which will be removed')

	parser_list = subparsers.add_parser('list', help='list playlists', usage='ytsync list')

	parser_get = subparsers.add_parser('get', help='download a playlist to a given dir', usage='ytsync get <url> <dir>')
	parser_get.add_argument('url', type=str, help='url of the playlist which will be downloaded')
	parser_get.add_argument('dir', type=str, help='directory in which the playlist will be downloaded')

	parser_sync = subparsers.add_parser('sync', help='sync a playlist with a given dir', usage='ytsync sync <name> <dir>')
	parser_sync.add_argument('name', type=str, help='name of the playlist which will be synced')
	parser_sync.add_argument('dir', type=str, help='directory with which the playlist will be synced')

	args = parser.parse_args()
	return args

if __name__ == '__main__':
	args = usage()
	if args.command == 'add':
		add_playlist(args.name, args.url)
	elif args.command == 'remove':
		remove_playlist(args.name)
	elif args.command == 'list':
		list_playlists_from_db()
	elif args.command == 'get':
		#download_playlist(args.name, args.dir)
		#get_video_meta(args.name, 'test_dir')
		download_playlist(args.url, args.dir)
	elif args.command == 'sync':
		sync_playlist(args.name, args.dir)
	
	#print (make_string_printable('rr83uwtfv8日本j94:&*/\\'))
	#print (filter_filename('r83uwtfv8日本j94:&*/\\'))