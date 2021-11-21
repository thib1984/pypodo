"""
Pypodo scripts
"""

import re
from columnar import columnar
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
    headers = ["index","task","tags"]
    data = []
    with open(todofilefromconfig(), "r") as todofile:
        for line in todofile.readlines():
            search = compute_args().search
            if re.findall(search, line.rstrip("\n")):
                data.append(printlinetodo(line))
                empty = False
    if empty:
        printwarning("the filtered todolist is empty")
    else:
        table = columnar(data, headers, no_borders=False, wrap_max=0)
        print(table)       