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
    read_config_boolean
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
        if compute_args().condensate:
            table = columnar(data, no_borders=True, wrap_max=0)
        else:
            if (read_config_boolean("FONCTIONAL", "condensate", "False")== "True"):
                table = columnar(data, no_borders=True, wrap_max=0)
            else:    
                table = columnar(data, headers, no_borders=False, wrap_max=0)            
        print(table)    