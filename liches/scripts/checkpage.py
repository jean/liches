import subprocess
import string
import random
import os
import sys
import emptydb
import importcsv

from ..utils import invalid_url

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> <url>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 3:
        usage(argv)
    if invalid_url(argv[2]):
        print invalid_url(argv[2])
        sys.exit(1)
    filename = ''.join(random.sample(
        string.ascii_letters + string.digits, 16)) + '.csv'
    subprocess.call(["bin/linkchecker",
                    "--recursion-level=1",
                    "--file-output=csv/utf-8/" + filename,
                    "--no-warnings",
                    "--pause=3",
                    argv[2]])
    emptydb.main(argv)
    argv[2] = filename
    importcsv.main(argv)
    os.remove(filename)
