import string, os, re, pafy, sys, glob, time
 
REFRESH_TIME = 600

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
        vid_name = elements[:-4]
        if not (os.path.exists(self.dir_do_dl+vid_name+".ogg") or \
                os.path.exists(self.dir_do_dl+vid_name+".m4a") or \
                os.path.exists(self.dir_do_dl+vid_name+".mp3")):
            return False
        return True

    def download_playlist(self):
        counter = 0
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
        print ('Syncing YouTube playlist [' + \
            self.filter_string_sequence(playlist['title']) +'] '+'('+ \
            str(self.playlist_size)+' songs) '+'with ' + \
            self.filter_string_sequence(self.dir_do_dl))
        for videos in playlist['items']:
            try:
                counter += 1 
                stream = videos['pafy'].getbestaudio()
                if stream is not None:
                    stream._title = stream.generate_filename()
                    if self.is_song_downloaded(stream._title):
                        continue
                    print ('Downloading' + ' -> ' \
                        + self.filter_string_sequence(stream.filename))
                    stream.download(self.dir_do_dl)
                    self.files_to_convert = True
            except OSError:
                pass          
            except IOError:
                pass
            except ZeroDivisionError:
                pass
        print ('Done                                                ')
        print ('Songs downloaded:'+str(counter))
        print ('-----------------')
        return 0

    def delete_incomplete(self, path):
        a = glob.glob(path+"*.temp")
        for item in a:
            os.system('del "'+item+'"')

    def format_files(self, path):
        if self.files_to_convert:
            a = glob.glob(path+"*.m4a")+glob.glob(path+"*.ogg")
            for item in a:
                input_song = item
                output_song = item[:-4] + ".mp3"
                command = ('ffmpeg -i "' + input_song+'" "' + output_song+'"')
                os.system(command)
                os.system('del "'+item+'"')

while True:
    f = open('synclist.txt')
    for lines in f:
        if lines[:4] == 'http':
            url = lines[:-1]
            continue
        else:
            destination = lines[:-1]
        p = downloader(url,destination)
        p.download_playlist()

        p.delete_incomplete(p.dir_do_dl)
        #############p.format_files(p.dir_do_dl)
        del p
        
    f.close()
    time.sleep(REFRESH_TIME)
    




