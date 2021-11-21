"""
Pypodo scripts
"""

import re
from pypodo.config import (
    todofilefromconfig,
)
from pypodo.args import compute_args
from pypodo.print import (
    printwarning,
    printinfo,
)


def add(openfile=open):
    """
    Add a task to the todofile
    """
    with openfile(todofilefromconfig(), "r") as todofile:
        lines = todofile.readlines()
        # index calculation
        if len(lines) > 0:
            last_line = lines[len(lines) - 1]
            index = int(last_line.split()[0]) + 1
        else:
            index = 1
    with openfile(todofilefromconfig(), "a") as todofile:
        # loop on the indexes
        for task in compute_args().add:
            # check format : words* #tag1 #tag2 : task at free format,
            # tags in one word prefixed by #
            if not re.findall("^([^#]|([^ ]#))*( #[^ #]+)*$", task):
                printwarning(
                    "the task has not a valid format - " + task
                )
            else:
                # adding task to the todolist
                todofile.write(str(index) + " " + task + "\n")
                printinfo(
                    "task is added to the todolist - "
                    + str(index)
                    + " "
                    + task
                )
                index = index + 1
