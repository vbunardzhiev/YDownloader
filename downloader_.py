import argparse
import os
import sqlite3
import datetime
import pafy

db_filename = 'playlists.db'

def create_db():
	if not os.path.exists(db_filename):
		connection = sqlite3.connect(db_filename)
		db = connection.cursor()
		db.execute('''CREATE TABLE playlists
						(name text,
						 url text,
						 last_synced text)''')
		connection.commit()
		connection.close()
		return 0
	return 1

def add_playlist(playlist_name, playlist_url):
	connection = sqlite3.connect(db_filename)
	db = connection.cursor()
	playlist = str(playlist_name), str(playlist_url), '-'
	db.executemany('INSERT INTO playlists VALUES (?,?,?)', (playlist,))
	connection.commit()
	connection.close()

def remove_playlist(playlist_name):
	connection = sqlite3.connect(db_filename)
	db = connection.cursor()
	db.execute('DELETE FROM playlists WHERE name = ?', (playlist_name,))
	connection.commit()
	connection.close()

def get_playlist_url(playlist_name):
		connection = sqlite3.connect(db_filename)
		db = connection.cursor()
		db.execute('SELECT url FROM playlists WHERE name=?', (playlist_name,))
		result = db.fetchone()
		connection.close()
		return result

def list_playlists():
	connection = sqlite3.connect(db_filename)
	db = connection.cursor()
	for row in db.execute('select * from playlists'):
		print (row)
	connection.close()

def update_last_dl(playlist_name):
	connection = sqlite3.connect(db_filename)
	db = connection.cursor()
	time_now = str(datetime.datetime.now())[:19]
	db.execute('UPDATE playlists SET last_synced=? WHERE name=?', (time_now, playlist_name,))
	connection.commit()
	connection.close()

def usage():
	parser = argparse.ArgumentParser(usage='''ytsync <command> [<args>]''')
#         usage='''ytsync <command> [<args>]

# commands:
#    add       add a playlist
#    remove    remove a playlist
#    list      list all playlists
#    get       syncs a playlist with a given directory
#    ''')
	#parser.add_argument('--add', action='store_const', const=lambda:add_playlist(), dest='cmd')
	subparsers = parser.add_subparsers()

	parser_add = subparsers.add_parser('add', help='add playlist', usage='ytsync add <name> <url>')
	parser_add.add_argument('<name>', type=str, help='playlist name')
	parser_add.add_argument('<url>', type=str, help='playlist url')

	parser_remove = subparsers.add_parser('remove', help='remove playllist', usage='ytsync remove <name>')
	parser_remove.add_argument('<name>', type=str, help='name of the playlist which will be removed')

	parser_list = subparsers.add_parser('list', help='list playlists', usage='ytsync list')

	parser_get = subparsers.add_parser('get', help='syncs a playlist with a given dir', usage='ytsync get <name> <dir>')
	parser_get.add_argument('<name>', type=str, help='name of the playlist which will be downloaded')
	parser_get.add_argument('<dir>', type=str, help='directory in which the playlist will be downloaded')
	#parser.add_argument('--list', action='store_const', const=lambda:list_playlists(), dest='cmd')
	parser.parse_args()#.cmd()

def get():
	pass

if __name__ == '__main__':
	usage()




	# create_db()
	# add_playlist('shun', 'lala')
	# print (get_playlist_url('shun'))
	# update_last_dl('shun')
	# list_playlists()
