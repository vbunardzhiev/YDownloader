import sqlite3, os, datetime

class Playlists():
		def __init__(self, db_filename):
			self.db_file = str(db_filename)
			self.create_folder(db_filename)
			self.db_file = self.db_file + 'playlists'

		def create_folder(self, path):
			try:
				os.mkdir(path)
			except FileExistsError:
				pass

		def create_db(self):
			if not os.path.exists(self.db_file):
				connection = sqlite3.connect(self.db_file)
				db = connection.cursor()
				db.execute('''CREATE TABLE playlists
								(name text,
								 playlist_url text,
								 last_downloaded text)''')
				connection.commit()
				connection.close()
				return 0
			return 1

		def add_playlist(self, playlist_name, playlist_url):
			connection = sqlite3.connect(self.db_file)
			db = connection.cursor()
			playlist = str(playlist_name), str(playlist_url)
			db.executemany('INSERT INTO playlists VALUES (?,?)', (playlist,))
			connection.commit()
			connection.close()

		def remove_playlist(self, playlist_name):
			connection = sqlite3.connect(self.db_file)
			db = connection.cursor()
			db.execute('DELETE FROM playlists WHERE name = ?', (playlist_name,))
			connection.commit()
			connection.close()

		def get_playlists(self):
			all_playlists = {}
			i = 0
			connection = sqlite3.connect(self.db_file)
			db = connection.cursor()
			for row in db.execute('select * from playlists'):
				all_playlists[i] = row[0], row[1]
				i += 1
			connection.close()
			return all_playlists

		def get_playlist_url(self, playlist_name):
			all_playlists = []
			connection = sqlite3.connect(self.db_file)
			db = connection.cursor()
			db.execute('SELECT playlist_url FROM playlists WHERE name=?', (playlist_name,))
			result = db.fetchone()[0]
			connection.close()
			return result

		def update_last_dl(self, playlist_name):
			connection = sqlite3.connect(self.db_file)
			db = connection.cursor()
			time_now = str(datetime.datetime.now())[:19]
			db.execute('UPDATE playlists SET last_downloaded=? WHERE name=?', (time_now,playlist_name,))
			connection.commit()
			connection.close()

