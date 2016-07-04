import pafy
import requests
import json
import sys
import re
import string
import time
from threading import Thread
import threading
from functools import wraps
import urllib.parse

def run_async(func):
    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target = func, args = args, kwargs = kwargs)
        func_hl.start()
        return func_hl
    return async_func

def filter_filename(sequence):
    #printable_ = re.sub(r'[/\\:?"<>|*,&\'~`^\t\n\r\x0b\x0c]', '_', string.printable)
    ok = re.compile(r'[^/\\:?"<>|*,&\'~`^\t\n\r\x0b\x0c]')
    seq_ = "".join(x if ok.match(x) else "_" for x in sequence)
    return seq_

@run_async
def download_in_pcloud(auth, url, name):
    name = filter_filename(name)
    request = "http://api.pcloud.com/downloadfile?auth=" + auth + "&nopartial=1&folderid=271359118&target=" + name + "&url=" + urllib.parse.quote_plus(url)
    requests.get(request).json()

playlist = pafy.get_playlist(sys.argv[1])
palylist_len = len(playlist['items'])
count = 0
for video in playlist['items']:
    count += 1
    sys.stdout.write("\r" + ' {:.1%}'.format(count/palylist_len) + "\r")
    filename = filter_filename(video['playlist_meta']['title'])
    try:
        stream = video['pafy'].getbestaudio()
        if stream is not None:
            download_in_pcloud(auth="4PD1XkZfXwRZd08cDtWeePfr6nS5pyJDHmtQYYQ7", url=stream._url, name=stream.filename)

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

while threading.active_count() > 1:
	time.sleep(1)
print ('Done'.ljust(90))
print ('-----------------')
