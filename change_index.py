import glob, sys, os, re

def change_index(path, offset):
    pairs = []
    files = [song for song in glob.glob(path+'*.*')]
    for file in files:
        filename = os.path.split(file)[1]
        prefix = re.findall(r'[0-9]+', filename)[0]
        new_prefix = int(prefix) + offset
        new_prefix = '0'*(3-len(str(new_prefix))) + str(new_prefix)
        new_file = file.replace(prefix, new_prefix)

if __name__ == "__main__":
    change_index(sys.argv[1], sys.argv[2])
