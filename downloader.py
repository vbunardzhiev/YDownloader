import string, os, re, sys, glob, time, subprocess, re
from PlaylistsDB import Playlists
import pafy


class Downloader():
    def __init__(self,url,path):
        self.allowed_symbols = re.sub('[/\\:?"<>|*]', '_', string.printable)
        self.playlist_author = ''
        self.playlist_title = ''
        self.playlist_size = 0
        self.playlist_url = url
        self.dir_to_dl = path
        self.is_there_playlist_obj = False
        pafy.set_api_key('AIzaSyBHkNTjYXIDMR7TdoR7ZqgNiymYgvvt_pE')

    def filter_string_sequence(self,sequence):
        for chars in sequence:
            if chars not in self.allowed_symbols:
                sequence = re.sub(re.escape(chars),'_',sequence)
            if len(sequence) > 80:
                sequence = sequence[:40] + '..' + sequence[55:]
        return sequence

    def create_playlist_object(self):
        try:
            playlist = pafy.get_playlist(self.playlist_url)
            self.playlist_title = playlist['title']
            self.playlist_author = playlist['author']
            self.playlist_size = len(playlist['items'])
            if not self.is_there_playlist_obj:
                self.dir_to_dl = self.dir_to_dl +'@'+self.playlist_author+'  #' \
                               + self.playlist_title+'\\'
                self.is_there_playlist_obj = True
            if not os.path.exists(self.dir_to_dl):
                os.makedirs(self.dir_to_dl)
            return playlist
        except FileNotFoundError:
            return False

    def is_url_real(self):
        try:
            playlist = pafy.get_playlist(self.playlist_url)
            return True
        except ValueError:
            return False
        except OSError:
            return False

    def is_song_downloaded(self,elements):
        filename = elements[:-4]
        if not (os.path.exists(self.dir_to_dl+filename+".ogg") or \
                os.path.exists(self.dir_to_dl+filename+".m4a") or \
                os.path.exists(self.dir_to_dl+filename+".mp3")):
            return False
        return True

    def download_playlist(self):
        song_count = 0
        if not self.is_url_real():
            return 1
        if not self.create_playlist_object():
            return 2
        playlist = self.create_playlist_object()
        print ('Syncing YouTube playlist [' + \
            self.filter_string_sequence(playlist['title']) +'] '+'('+ \
            str(self.playlist_size)+' songs) '+'with ' + \
            self.filter_string_sequence(self.dir_to_dl))
        for videos in playlist['items']:
            try:
                song_count += 1
                stream = videos['pafy'].getbestaudio()
                if stream is not None:
                    stream._title = stream.generate_filename()
                    if self.is_song_downloaded(stream._title):
                        continue
                    stream._title = stream._title[:-4]
                    print ('Downloading' + ' -> ' \
                        + self.filter_string_sequence(stream.filename).ljust(90)
                        + str(song_count) + '/' + str(self.playlist_size))
                    stream.download(filepath=self.dir_to_dl, meta=True)
            except OSError:
                pass
            except IOError:
                pass
            except ZeroDivisionError:
                pass
            except KeyError:
                pass
            except IndexError:
                pass
            except AttributeError:
                pass
        print ('Done'.ljust(90))
        print ('-----------------')
        return 0

    def delete_incomplete_files(self, path):
        incomplete_files = glob.glob(path + "*.temp")
        for item in incomplete_files:
            os.system('del "'+item+'"')

    def return_paired_files(self, path, audio_format):
        pairs = []
        other_files = [song for song in glob.glob(path+'*.*')
                       if song[-3:] != audio_format]
        for item in other_files:
            input_song = item
            output_song = item[:-4] + '.' + audio_format
            pairs.append((input_song, output_song))
        return pairs

    def detect_audio_level(self, audio_file):
        new_file = audio_file.rpartition('\\')[0] + '\\' + 'item1' +  '.' + audio_file.rpartition('.')[2]
        os.rename(audio_file, new_file)
        command_ = 'ffmpeg -i "'+ new_file+ '" -af "volumedetect" -f null /dev/null'
        cmd_output = subprocess.getoutput(command_)
        first_match = re.findall('max_volume: ' + r'.+' , cmd_output)[0]
        os.rename(new_file, audio_file)
        return -float(re.findall(r'-?[0-9]{1,3}[.][0-9]{1}', first_match)[0])


    def format_files(self, path, audio_format, delete_original_files=True):
        if not self.create_playlist_object():
            return 2
        ### It formats only the non-formated files. ###
        current = 1
        in_and_out_files = self.return_paired_files(self.dir_to_dl, audio_format)
        if in_and_out_files != []:
            print ('Transcoding audio files. Do not interrupt!')
            sys.stdout.write("\r" + ' 0.00%' + "\r")
        for input_song, output_song in in_and_out_files:
            sys.stdout.flush()
            sound_difference = (self.detect_audio_level(input_song))
            os.system('ffmpeg -loglevel quiet -i "' + input_song+'" -af volume=' + str(sound_difference) + 'dB "' + output_song+'"')
            sys.stdout.write("\r" + ' {:.2%}'.format(current/len(in_and_out_files)) + "\r")
            current += 1
            if delete_original_files:
                os.system('del "'+input_song+'"')


if __name__ == "__main__":
    playlist_db = Playlists('C:\\Users\\User\\AppData\\Local\\playlists_db\\')
    playlist_db.create_db()
    url = playlist_db.get_playlist_url(sys.argv[1])
    directory = sys.argv[2]
    p = Downloader(url,directory)
    p.download_playlist()
    p.delete_incomplete_files(directory)
    if len(sys.argv) > 3:
        file_format = sys.argv[3]
        p.format_files(directory, file_format, True)
    del p
