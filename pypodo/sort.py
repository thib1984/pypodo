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

from pypodo.print import (
    printwarning,
    printinfo,
)


def sort(openfile=open):
    """
    Reorder the todofile with consecutives indexes
    """
    empty = True
    index = 1
    with openfile(todofilefromconfig(), "r") as todofile:
        lines = todofile.readlines()
    with openfile(todofilefromconfig(), "w") as todofile:
        for line in lines:
            # we replace the existing index by the current index that we increment
            replaced = re.sub("^\\d+ ", str(index) + " ", line)
            index = index + 1
            todofile.write(replaced)
            empty = False
    if empty:
        printwarning("the todolist is empty - nothing to do")
    else:
        printinfo("the todolist is sorted")
