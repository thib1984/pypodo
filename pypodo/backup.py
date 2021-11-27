"""
Pypodo scripts
"""

import os
import sys
import time
from shutil import copyfile

from pypodo.config import (
    todofilefromconfig,
    todobackupfolderfromconfig,
)
from pypodo.print import (
    printinfo,
    printerror,
)


def backup(openfile=open):
    """
    Backup the todofile
    """
    dir_exists = os.path.exists(todobackupfolderfromconfig())
    if not dir_exists:
        try:
            os.makedirs(todobackupfolderfromconfig())
        except PermissionError:
            printerror(
                "permission error to create the backup folder : "
                + todobackupfolderfromconfig()
            )
            sys.exit()
        printinfo("creating todolist backup folder")
    time_suffix = time.strftime("%Y%m%d%H%M%S")
    todo_backup_name = "todo" + time_suffix
    backup_name = os.path.join(todobackupfolderfromconfig(),todo_backup_name)
    try:
        copyfile(todofilefromconfig(), backup_name)
    except PermissionError:
        printerror(
            "permission error to create the backup folder : "
            + todobackupfolderfromconfig()
        )
        sys.exit()
    printinfo("creating todolist backup - " + backup_name)
