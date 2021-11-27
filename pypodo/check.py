"""
Pypodo scripts
"""

import os
import re
import sys
from pypodo.config import (
    todofilefromconfig
)

from pypodo.print import (
    printwarning,
    printinfo,
    printerror,
)



def check(openfile=open):
    """
    Check the toodofile
    """
    file_exists = os.path.isfile(todofilefromconfig())
    if file_exists:
        try:
            with openfile(todofilefromconfig(), "r") as todofile:
                error = False
                for line in todofile.readlines():
                    # verification regex, index + task + possible tags
                    if not re.findall(
                        "^\\d+ ([^#]|([^ ]#))*( #[^ #]+)*$",
                        line.rstrip("\n"),
                    ):
                        printwarning(
                            "this line has not a valid format in todo file - "
                            + line.rstrip("\n")
                        )
                        error = True
            if error:
                printerror("verify the todo file.")
                sys.exit()
            return True
        except PermissionError:
            printerror(
                "permission error to open the todofile : "
                + todofilefromconfig()
            )
            sys.exit()

    printinfo("creating todo file")
    try:
        f = openfile(todofilefromconfig(), "a")
        f.close
    except FileNotFoundError:
        printerror(
            "the path "
            + todofilefromconfig()
            + " does not exist, correct it (in the config file)"
        )
        sys.exit()
    return True
