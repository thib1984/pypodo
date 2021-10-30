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
    printinfo,
    printerror,
)



def tag(openfile=open):
    """
    Tag tasks from the todofile
    """
    if len(compute_args().tag) >= 2:
        tagtoadd = compute_args().tag[0]
        if not re.findall("^[^ #]+$", tagtoadd):
            printerror("the tag has not a valid format - " + tagtoadd)
        else:
            # loop on the indexes
            for increment in range(1, len(compute_args().tag)):
                index = compute_args().tag[increment]
                # check the numeric format of the index
                if re.findall(REGEX_INDEX, index):
                    tagone(index, tagtoadd, openfile)
                elif re.findall("^\\d+-\\d+$", index) and int(
                    index.split("-")[0]
                ) < int(index.split("-")[1]):
                    for indexlist in range(
                        int(index.split("-")[0]),
                        int(index.split("-")[1]) + 1,
                    ):
                        tagone(str(indexlist), tagtoadd, openfile)
                else:
                    printwarning(
                        "the index to tag is not in numeric format - "
                        + index
                    )

    else:
        printerror(
            "2 or more parameters is needed for pypodo tag : the tag to add and"
            " the indexes of the task whose tags to add"
        )


def tagone(index, tagtoadd, openfile):
    """
    Tag on task
    """
    index_trouve = False
    with openfile(todofilefromconfig(), "r") as todofile:
        lines = todofile.readlines()
    with openfile(todofilefromconfig(), "w") as todofile:
        for line in lines:
            if not re.findall("^" + index + " ", line):
                todofile.write(line)
            else:
                newline = line.rstrip("\n") + " #" + tagtoadd
                todofile.write(newline + "\n")
                printinfo(
                    "tag added to the task of the todolist - "
                    + line.rstrip("\n")
                    + " -> "
                    + newline.rstrip()
                )
                index_trouve = True
    if not index_trouve:
        printwarning("no task with index - " + index)

