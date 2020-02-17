import platform
import urllib.request
import os
import sys

os_type = platform.system()
print(os_type)

# Assume Windows
url = 'https://sourceforge.net/projects/libroadrunner/files/libroadrunner-1.4.18/roadrunner-win64-vs14-cp35m.zip/download'

if os_type == 'Darwin':
  url = 'https://sourceforge.net/projects/libroadrunner/files/libroadrunner-1.4.18/roadrunner-osx-10.9-cp36m.tar.gz/download'

fname = url.split('/')[-2]

print('Beginning download of libroadrunner into your home directory...')
print(url)

home = os.path.expanduser("~")
my_file = os.path.join(home, fname)

print('home = ',home)

def download_cb(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

urllib.request.urlretrieve(url, my_file, download_cb)


