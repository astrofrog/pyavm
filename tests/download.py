import os
import urllib
import multiprocessing as mp

from pyavm import AVM

N_PROCESSES = 16


def download(url):

    # Get rid of any whitespace
    url = url.strip()

    # Find output filename
    filename = os.path.basename(url)

    # Open URL and download file
    try:
        u = urllib.urlopen(url.strip())
        open('images/%s' % filename, 'wb').write(u.read())
        return True
    except:
        return False

# Make sure that images directory exists
if not os.path.exists('images'):
    os.mkdir('images')

# Find URLs to donwload
urls = open('example_urls.txt', 'rb').readlines()

# Download files using multiple threads
p = mp.Pool(processes=N_PROCESSES)
succeeded = p.map(download, urls)

# Check if any downloads failed
for i in range(len(urls)):
    if not succeeded[i]:
        print "Failed: %s" % urls[i]
