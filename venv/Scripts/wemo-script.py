#!C:\Users\maxak\Dropbox\Zoos\Interlock\python\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'ouimeaux==0.8','console_scripts','wemo'
__requires__ = 'ouimeaux==0.8'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('ouimeaux==0.8', 'console_scripts', 'wemo')()
    )
