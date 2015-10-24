import subprocess
pesen = 'C:\\Users\\User\\Desktop\\F.O. & ЯВКАТА ДЛГ - 100 ГОДИНИ (prod. FB).mp3'
pesen_ = 'C:\\Users\\User\\Desktop\\test.mp3'
pesen.encode('utf-8')
command = ['ffmpeg', '-i', pesen, '-af', 'volumedetect', '-f', 'null', 'NULL']
command_ = 'ffmpeg -i ' + pesen_ + ' -af volumedetect -f null NULL'
#print (subprocess.getoutput(command_))
p=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
text = p.stderr.read()
retcpde=p.wait()
text = text.encode(errors='replace')
print (text)
