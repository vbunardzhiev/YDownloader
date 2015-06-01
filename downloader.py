import string, os, re, sys, glob, time
import pafy

READY = 0

class Downloader():
    def __init__(self,url,path):
        self.allowed_symbols = re.sub('[/\\:?"<>|*]', '_', string.printable)
        self.playlist_author = ''
        self.playlist_title = ''
        self.playlist_size = 0
        self.playlist_url = url
        self.dir_to_dl = path
        pafy.set_api_key('AIzaSyBHkNTjYXIDMR7TdoR7ZqgNiymYgvvt_pE')
        
    def filter_string_sequence(self,sequence):
        for chars in sequence:
            if chars not in self.allowed_symbols:
                sequence = re.sub(re.escape(chars),'_',sequence)
            if len(sequence) > 80:
                sequence = sequence[:40] + '..' + sequence[55:]
        return sequence

    def path_check(self):
        try:
            if not os.path.exists(self.dir_to_dl):
                os.makedirs(self.dir_to_dl)
            return True
        except FileNotFoundError:
            return False

    def url_check(self):
        try:
            playlist = pafy.get_playlist(self.playlist_url)
            return True
        except ValueError:
            return False
        except OSError:
            return False

    def is_song_downloaded(self,elements):
        vid_name = elements[:-4]
        if not (os.path.exists(self.dir_to_dl+vid_name+".ogg") or \
                os.path.exists(self.dir_to_dl+vid_name+".m4a") or \
                os.path.exists(self.dir_to_dl+vid_name+".mp3")):
            return False
        return True

    def download_playlist(self):
        song_count = 0
        if not self.url_check():
            return 1
        playlist = pafy.get_playlist(self.playlist_url)
        self.playlist_title = playlist['title']
        self.playlist_author = playlist['author']
        self.playlist_size = len(playlist['items'])
        self.dir_to_dl = self.dir_to_dl +'@'+self.playlist_author+'  #' \
            + self.playlist_title+'/'
        if not self.path_check():
            return 2
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
                    stream.download(self.dir_to_dl)
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
            # except ValueError:
            #     pass

        print ('Done'.ljust(90))
        print ('-----------------')
        return 0

    def delete_incomplete(self, path):
        a = glob.glob(path+"*.temp")
        for item in a:
            os.system('del "'+item+'"')

    def format_files(self, path):
        ### If called after script has finished DL, it formats the non-formated files. ###
        current = 0
        print ('Transcoding audio files. Do not interrupt!')
        sys.stdout.write("\r" + ' 0.00%' + "\r")
        sys.stdout.flush()
        a = glob.glob(path+"*.m4a")+glob.glob(path+"*.ogg")
        for item in a:
            input_song = item
            output_song = item[:-4] + ".mp3"
            os.system('ffmpeg -loglevel quiet -i "' + input_song+'" "' + output_song+'"')
            current += 1
            sys.stdout.write("\r" + ' {:.2%}'.format(current/len(a)) + "\r")
            sys.stdout.flush()
            os.system('del "'+item+'"')

#while READY == 0:
f = open(sys.argv[1])
for lines in f:
    if lines[:4] == 'http':
        url = lines[:-1]
        continue
    else:
        destination = lines[:-1]
    p = Downloader(url,destination)
    p.download_playlist()

    p.delete_incomplete(p.dir_to_dl)
    p.format_files(p.dir_to_dl)
    del p
f.close()