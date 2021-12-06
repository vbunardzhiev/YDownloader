import os
import sqlite3
import datetime

db_filename = 'playlists.db'

def create_db():
	if not os.path.exists(db_filename):
		try:
			connection = sqlite3.connect(db_filename)
			db = connection.cursor()
			db.execute('''CREATE TABLE playlists
							(name text,
							 url text,
							 last_dl text)''')
			connection.commit()
			return 0
		finally:
			connection.close()
		
	return 1

def playlist_exists(playlist_name):
	try:
		connection = sqlite3.connect(db_filename)
		db = connection.cursor()
		db.execute('SELECT name FROM playlists WHERE name = ?', (playlist_name,))
		data = db.fetchone()
	finally:
		connection.close()
	if data:
		return True
	else:
		return False

def add_playlist(playlist_name, playlist_url):
	create_db()
	if not playlist_exists(playlist_name):
		try:
			connection = sqlite3.connect(db_filename)
			db = connection.cursor()
			playlist = str(playlist_name), str(playlist_url), '-'
			db.executemany('INSERT INTO playlists VALUES (?,?,?)', (playlist,))
			connection.commit()
			print ('\nPlaylist "{}" added.'.format(playlist_name))
		finally:
			connection.close()
	else:
		print ('\nThere is already a playlist with that name!')

def remove_playlist(playlist_name):
	if playlist_exists(playlist_name):
		try:
			connection = sqlite3.connect(db_filename)
			db = connection.cursor()
			db.execute('DELETE FROM playlists WHERE name = ?', (playlist_name,))
			connection.commit()
			print ('\nPlaylist "{}" removed.'.format(playlist_name))
		finally:
			connection.close()
	else:
		print ('\nNo playlist "{}"'.format(playlist_name))

def get_playlist_url(playlist_name):
	try:
		connection = sqlite3.connect(db_filename)
		db = connection.cursor()
		db.execute('SELECT url FROM playlists WHERE name=?', (playlist_name,))
		result = db.fetchone()
		return result[0]
	finally:
		connection.close()

def list_playlists():
	try:
		connection = sqlite3.connect(db_filename)
		db = connection.cursor()
		playlists = []
		for row in db.execute('select * from playlists'):
			playlists.append(row)
		return playlists
	except sqlite3.OperationalError:
		print ('\ndb not created yet!')
	finally:
		connection.close()

def update_last_dl(playlist_name):
	try:
		connection = sqlite3.connect(db_filename)
		db = connection.cursor()
		time_now = str(datetime.datetime.now())[:19]
		db.execute('UPDATE playlists SET last_dl=? WHERE name=?', (time_now, playlist_name,))
		connection.commit()
		return 0
	finally:
		connection.close()
