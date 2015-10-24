import sqlite3, os

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
											(name text, playlist_url text)''')
				connection.commit()
				connection.close()
				return 0
			return 1

		def insert_playlist(self, playlist_name, playlist_url):
			connection = sqlite3.connect(self.db_file)
			db = connection.cursor()
			playlist = str(playlist_name), str(playlist_url)
			db.executemany('INSERT INTO playlists VALUES (?,?)', (playlist,))
			connection.commit()
			connection.close()

		def get_playlists(self):
			all_playlists = []
			connection = sqlite3.connect(self.db_file)
			db = connection.cursor()
			for row in db.execute('select * from playlists'):
					all_playlists.append(row[0])
			connection.close()
			return all_playlists

		def get_playlist_url(self, playlist_name):
			all_playlists = []
			connection = sqlite3.connect(self.db_file)
			db = connection.cursor()
			db.execute('select playlist_url from playlists where name=?', (playlist_name,))
			result = db.fetchone()[0]
			connection.close()
			return result