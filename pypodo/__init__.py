"""
Pypodo scripts
"""

import argparse
import os
import re
import sys
import time
import base64
import hashlib
from pathlib import Path
from shutil import copyfile
from datetime import datetime
from datetime import date
from pypodo.properties import (
    REGEX_INDEX,
    REGEX_SPACE_OR_ENDLINE,
)
from pypodo.config import (
    read_config,
    read_config_boolean,
    read_config_color,
    read_config_date_format,
    read_config_int,
    read_config_level,
    todofilefromconfig,
    todobackupfolderfromconfig,
)
from termcolor import colored
from pypodo.args import compute_args
from pypodo.update import update
from pypodo.version import version
from pypodo.print import (
    printdebug,
    printwarning,
    printinfo,
    printlinetodo,
    printerror,
)
from pypodo.check import check
from pypodo.list import listtask
from pypodo.add import add
from pypodo.delete import delete
from pypodo.sort import sort
from pypodo.untag import untag
from pypodo.tag import tag
from pypodo.backup import backup
from pypodo.search import find

# entrypoint
def pypodo(openfile=open):
    """
    Entrypoint
    """
    compute_args()
    if check(openfile):
        if compute_args().filter:
            listtask(openfile)
        elif compute_args().add:
            add(openfile)
        elif compute_args().delete:
            delete(openfile)
        elif compute_args().order:
            sort(openfile)
            listtask(openfile)
        elif compute_args().untag:
            untag(openfile)
        elif compute_args().tag:
            tag(openfile)
        elif compute_args().backup:
            backup(openfile)
        elif compute_args().search:
            find(openfile)
        elif compute_args().info:
            version()
        elif compute_args().update:
            update()
        else:
            listtask(openfile)



