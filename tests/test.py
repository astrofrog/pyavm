import glob
import os
import urllib

from pyavm import AVM

if not os.path.exists('images'):
    raise Exception("images/ does not exist - either run download.py first, or use the remote testing script test_remote.py")

for filename in glob.glob(os.path.join('images/', '*')):
    print "-" * 30
    print "Testing %s" % os.path.basename(filename)
    try:
        avm = AVM(filename)
        print "-> Parsing succeeded"
    except:
        print "-> Parsing failed"
