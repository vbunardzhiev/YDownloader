import os, glob


laina = {'0':'A', '1':'B', '2':'C', '3':'D', '4':'E', '5':'F', '6':'G', '7':'H', '8':'I', '9':'J'}
reverse_laina = {'A':'0', 'B':'1', 'C':'2', 'D':'3', 'E':'4', 'F':'5', 'G':'6', 'H':'7', 'I':'8', 'J':'9'}



os.chdir('D:\\Music\\@vasil bunardzhiev  #rap&hip hop\\')
p = glob.glob('*.mp3')
for item in p:
    number = 'AA' + item[:4] 
    lalala = ''
    for fakan_letyr in number:
        
        lalala = lalala + reverse_laina[fakan_letyr]
    new_name_shitstain = lalala + item[6:]
    os.rename(item, new_name_shitstain)