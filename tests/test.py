import os
import urllib

from pyavm import AVM

for url in open('example_urls.txt', 'rb'):
    image = urllib.urlopen(url.strip())
    print "-" * 30
    print "Downloading %s" % os.path.basename(url.strip())
    try:
        avm = AVM(image)
        print "-> Parsing succeeded"
    except:
        print "-> Parsing failed"