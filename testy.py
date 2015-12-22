import glob,re,os

path = 'H:\\@vasil bunardzhiev  #zzz\\*.mp3'
regex = r'[0-9]+'

for file_ in glob.glob(path):
    number = re.findall(regex, file_)[0]
    number_len = len(number)
    new_prefix = (4-number_len) * '0' + number
    new_filename = file_.replace(number, new_prefix)
    os.rename(file_, new_filename)

# THIS SHITFACE SCRIPT IS SO BUGGY. NEED TO REWRITE IT !!!