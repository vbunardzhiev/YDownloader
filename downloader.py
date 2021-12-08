import string, os, re, sys, glob, subprocess, pafy
from pafy.util import xenc
from urllib.error import HTTPError

class Downloader():
    def __init__(self,url,path):
        self.dir_to_dl = path

    def make_string_printable(self, string_, trunc=None):
        for chars in string_:
            if chars not in string.printable:
                string_ = re.sub(re.escape(chars), '_', string_)
        if trunc:
            if len(string_) > 49:
                trunc = len(string_) - 49
                l = int((len(string_) - trunc - 3) / 2)
                return '{}..{}'.format(string_[:l+10], string_[-l+10:])
        return string_

    def filter_filename(self, filename):
        ok = re.compile(r'[^\\/:*?"<>|]')
        seq_ = "".join(x if ok.match(x) else "_" for x in xenc(filename))
        return seq_

    def download_playlist(self, url, dir_):
        count = 0
        if not os.path.exists(dir_):
            os.makedirs(dir_)
        playlist = pafy.get_playlist2(url)
        playlist_title = self.make_string_printable(playlist.title)
        print ('\nDownloading playlist: [{}]'.format(playlist_title))
        for video in playlist:
            count += 1
            try:
                bestaudio = video.getbestaudio()
            except OSError:
                continue # Different restrictions: age, country, deleted profile, etc. 
            filename_witn_index = '0'*(3-len(str(count))) + str(count) + ' ' + bestaudio.filename
            filename = self.filter_filename(filename_witn_index)
            filepath = '{}\\{}'.format(dir_, filename)
            if self.is_song_downloaded(filepath):
                print ('Skipping: {}'.format(self.make_string_printable(video.title, trunc=46)).ljust(70) + '{}/{}'.format(count, playlist._len))
                continue
            print ('Downloading: {}'.format(self.make_string_printable(video.title, trunc=46)).ljust(70) + '{}/{}'.format(count, playlist._len))
            try:
                bestaudio.download(filepath=filepath, callback=self.progress, quiet=True)
            except HTTPError:
                continue

    def progress(self, *params):
        perc = params[1]/params[0]
        pr = ' {:.2%}\r'.format(perc)
        sys.stdout.write(pr)
        sys.stdout.flush()

    def is_song_downloaded(self, file_path):
        ext = 'mp3'
        if os.path.isfile(file_path):
            return True
        file_path_no_ext = file_path.rpartition('.')[0]
        mp3_filepath = '{}.{}'.format(file_path_no_ext, ext)
        if os.path.isfile(mp3_filepath):
            return True
        return False

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
            sound_difference = self.detect_audio_level(input_song)
            os.system('ffmpeg -n -loglevel quiet -i "' + input_song+'" -af volume=' + str(sound_difference) + 'dB "' + output_song+'"')
            sys.stdout.write('\r {:.2%}\r'.format(current/len(in_and_out_files)))
            current += 1
            if delete_original_files:
                os.remove(input_song)

if __name__ == "__main__":
    p = Downloader(sys.argv[1], sys.argv[2])
    p.download_playlist(sys.argv[1], sys.argv[2])
    p.format_files(sys.argv[2], "mp3", True)
del p
