"""
Pypodo scripts
"""

import re
from pypodo.properties import (
    REGEX_SPACE_OR_ENDLINE,
)
from pypodo.config import (
    todofilefromconfig,
)
from pypodo.args import compute_args
from pypodo.print import (
    printwarning,
    printlinetodo,
)



def listtask(openfile=open):
    """
    Print the todofile with filters or not
    """
    empty = True
    with openfile(todofilefromconfig(), "r") as todofile:
        for line in todofile.readlines():
            # without filter -> we print all
            if not compute_args().filter:
                printlinetodo(line)
                empty = False
            # with filter -> we check tag
            else:
                display = True
                for tagtofilter in compute_args().filter:
                    # regex to search tags "#toto " or "#toto" at the end of the line
                    if not re.findall(
                        " #"
                        + re.escape(tagtofilter)
                        + REGEX_SPACE_OR_ENDLINE,
                        line.rstrip("\n"),
                    ):
                        display = False
                if display:
                    printlinetodo(line)
                    empty = False
    if empty:
        if compute_args().filter:
            printwarning("the filtered todolist is empty")
        else:
            printwarning("the todolist is empty")

