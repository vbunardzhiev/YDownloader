import string, os, re, sys, glob, time, subprocess, re
import pafy
import requests
import json


class Downloader():
    def __init__(self,url,path):
        self.allowed_symbols = re.sub('[/\\:?"<>|*]', '_', string.printable)
        self.playlist_author = ''
        self.playlist_title = ''
        self.playlist_size = 0
        self.playlist_url = url
        self.dir_to_dl = path
        self.is_there_playlist_obj = False
        #pafy.set_api_key('AIzaSyBHkNTjYXIDMR7TdoR7ZqgNiymYgvvt_pE') #AIzaSyBHkNTjYXIDMR7TdoR7ZqgNiymYgvvt_pE

    def run_async(func):
        from threading import Thread
        from functools import wraps

        @wraps(func)
        def async_func(*args, **kwargs):
            func_hl = Thread(target = func, args = args, kwargs = kwargs)
            func_hl.start()
            return func_hl

        return async_func

    def filter_filename(self,sequence):
        ok = re.compile(r'[^\\/:*?"<>|]')
        seq_ = "".join(x if ok.match(x) else "_" for x in sequence)
        return seq_

    def filter_string_sequence_printable(self,sequence):
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

    def is_song_downloaded(self ,filename):
        pattern = self.dir_to_dl + '*{}.*'.format(glob.escape(filename))
        files_list = glob.glob(pattern)
        if len(files_list):
            return True
        return False

    def download_playlist(self, del_all):
        if not self.is_url_real():
            return 1
        if not self.create_playlist_object():
            return 2
        if del_all:
            self.delete_dir(self.dir_to_dl)
        song_count = 0
        playlist = self.create_playlist_object()
        print ('Syncing YouTube playlist [' + \
            self.filter_string_sequence_printable(playlist['title']) +'] '+'('+ \
            str(self.playlist_size)+' songs) '+'with ' + \
            self.filter_string_sequence_printable(self.dir_to_dl))

        for video in playlist['items']:
            filename = self.filter_filename(video['playlist_meta']['title'])
            song_count += 1

            count_len = len(str(song_count))
            if self.is_song_downloaded(filename):
                print ('Skipping [already downloaded] {}'.format(self.filter_string_sequence_printable(filename)))
                self.update_file_index(filename, song_count)
                continue

            try:
                stream = video['pafy'].getbestaudio()
                if stream is not None:
                    new_name = self.dir_to_dl + '\\' + '0'*(6-count_len) + str(song_count) + ' ' + stream.filename
                    print ('Downloading' + ' -> ' \
                        + self.filter_string_sequence_printable(new_name.rpartition('\\')[2]).ljust(90)
                        + str(song_count) + '/' + str(self.playlist_size))
                    stream.download(filepath=self.dir_to_dl, meta=True)
                    os.rename(self.dir_to_dl + '\\' + stream.filename, new_name)

            except TypeError:
                print ('TypeError')
                pass
            except OSError:
                print ('OSError')
                pass
            except IOError:
                print ('IOError')
                pass
            except ZeroDivisionError:
                print ('ZeroDivisionError')
                pass
            except KeyError:
                print ('KeyError')
                pass
            except IndexError:
                print ('IndexError')
                pass
            except AttributeError:
                print ('AttributeError')
                pass
        print ('Done'.ljust(90))
        print ('-----------------')
        return 0

    @run_async
    def download_in_pcloud(self, auth, url, name):
        import urllib.parse
        request = "http://api-sf1.pcloud.com/downloadfile?auth=" + auth + "&nopartial=1&folderid=271359118&target=" + name + "&url=" + urllib.parse.quote_plus(url)
        requests.get(request).json()

    def delete_incomplete_files(self, path):
        incomplete_files = glob.glob(path + "*.temp")
        for item in glob.glob(path + "item1.*"):
            incomplete_files.append(item)        
        for item in incomplete_files:
            os.remove(item)

    def return_paired_files(self, path, audio_format):
        pairs = []
        other_files = [song for song in glob.glob(path+'*.*')
                       if song.rpartition('.')[2] != audio_format]
        for item in other_files:
            input_song = item
            output_song = item.rpartition('.')[0] + '.' + audio_format
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
        # if not self.create_playlist_object():
        #     return 2
        ### It formats only the non-formated files. ###
        current = 1
        in_and_out_files = self.return_paired_files(self.dir_to_dl, audio_format)
        if in_and_out_files != []:
            print ('Transcoding audio files. Do not interrupt!')
            sys.stdout.write("\r" + ' 0.00%' + "\r")
        for input_song, output_song in in_and_out_files:
            sys.stdout.flush()
            sound_difference = self.detect_audio_level(input_song)
            os.system('ffmpeg -n -loglevel quiet -i "' + input_song+'" -af volume=' + str(sound_difference) + 'dB "' + output_song+'"')
            sys.stdout.write("\r" + ' {:.2%}'.format(current/len(in_and_out_files)) + "\r")
            current += 1
            if delete_original_files:
                os.remove(input_song)




    def update_file_index(self, filename, index):
        pattern = self.dir_to_dl + '*{}.*'.format(glob.escape(filename))
        file_to_rename = glob.glob(pattern)[0]
        count_len = len(str(index))
        new_index = '0'*(6-count_len) + str(index)
        old_index = file_to_rename.rpartition('\\')[2][:6]
        new_filename = file_to_rename[:].replace(old_index, new_index)
        os.rename(file_to_rename, new_filename)

    def delete_dir(self, dir_):
        for the_file in os.listdir(dir_):
            file_path = os.path.join(dir_, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)


if __name__ == "__main__":
    p = Downloader('PLe5NT0OhEv1OuKaNUDH8_dIp5QWbeWV4I', "C:\\Users\\bunar\\Desktop\\music\\music\\bg\\")
    p.format_files("C:\\Users\\bunar\\Desktop\\music\\music\\bg\\", "mp3", True)
del p
