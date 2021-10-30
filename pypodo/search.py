"""
Pypodo scripts
"""

import re
from pypodo.properties import (
    REGEX_INDEX,
)
from pypodo.config import (
    todofilefromconfig,
)
from pypodo.args import compute_args
from pypodo.print import (
    printwarning,
    printlinetodo,
)



def find(openfile=open):
    """
    Search with regex in the todofile
    """
    empty = True
    with open(todofilefromconfig(), "r") as todofile:
        for line in todofile.readlines():
            search = compute_args().search
            if re.findall(search, line.rstrip("\n")):
                printlinetodo(line)
                empty = False
    if empty:
        printwarning("the filtered todolist is empty")
