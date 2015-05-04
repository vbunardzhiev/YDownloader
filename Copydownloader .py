import string, os, re, pafy, sys, glob

class downloader():
    def __init__(self,url,path):
        self.allowed_symbols = re.sub('[/\\:?"<>|*]', '_', string.printable)
        self.files_to_convert = False
        self.current_file = 1
        self.playlist_author = ''
        self.playlist_title = ''
        self.playlist_size = 0
        self.playlist_url = url
        self.dir_do_dl = path
        #self.max_dl_speed = 0

    def filter_string_sequence(self,sequence):
        for chars in sequence:
            if chars not in self.allowed_symbols:
                sequence = re.sub(re.escape(chars),'_',sequence)
        return sequence

    def path_check(self):
        try:
            if not os.path.exists(self.dir_do_dl): 
                os.makedirs(self.dir_do_dl)
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
        vid_name = self.filter_string_sequence(elements)
        if not (os.path.exists(self.dir_do_dl+vid_name+".ogg") or \
                os.path.exists(self.dir_do_dl+vid_name+".m4a") or \
                os.path.exists(self.dir_do_dl+vid_name+".mp3")):
            return False
        return True

    def download_playlist(self):
        if not self.url_check():
            return 1
        playlist = pafy.get_playlist(self.playlist_url)
        self.playlist_title = playlist['title']
        self.playlist_author = playlist['author']
        self.playlist_size = len(playlist['items'])
        self.dir_do_dl = self.dir_do_dl +'@'+self.playlist_author+'  #' \
            + self.playlist_title+'/'
        if not self.path_check():
            return 2
        for videos in playlist['items']:
            if self.is_song_downloaded(videos['playlist_meta']['title']):
                continue
            try:
                #os.system('cls')
                stream = videos['pafy'].getbestaudio()
                if stream is not None:
                    stream._title = self.filter_string_sequence(stream.title)
                    print (stream._title + ' -> ' + playlist['title'])
                    stream.download(self.dir_do_dl)
                    self.files_to_convert = True
            except IOError:
                continue
            except ZeroDivisionError:
                return 4
        return 0

    def format_files(self, path):
        a = glob.glob(path+"*.m4a")#+glob.glob(path+"*.ogg")
        for item in a:
            input_song = item
            output_song = item[:-4] + ".mp3"
            command = ('ffmpeg -i "' + input_song+'" "' + output_song+'"')
            os.system(command)
            os.system('del "'+item+'"')
        a = glob.glob(path+"*.temp")
        for item in a:
            os.system('del "'+item+'"')

p = downloader('https://www.youtube.com/playlist?list=PL2E89F34B721F45B4','E:/Music/')

p.download_playlist()
p.format_files(p.dir_do_dl)