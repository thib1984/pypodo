"""
Pypodo scripts
"""

import re
from pypodo.properties import (
    REGEX_INDEX,
)
from pypodo.config import (
    read_config_boolean,
    todofilefromconfig,
)
from pypodo.args import compute_args
from pypodo.print import (
    printwarning,
    printinfo,
)


def delete(openfile=open):
    """
    Delete a task from the todofile
    """
    # loop on the indexes
    for index in compute_args().delete:
        # check the numeric format of the index
        if re.findall(REGEX_INDEX, index):
            deleteone(index, openfile)
        elif re.findall("^\\d+-\\d+$", index) and int(
            index.split("-")[0]
        ) < int(index.split("-")[1]):
            for indexlist in range(
                int(index.split("-")[0]),
                int(index.split("-")[1]) + 1,
            ):
                deleteone(str(indexlist), openfile)
        else:
            printwarning(
                "the index to delete is not in numeric format - "
                + index
            )

    if (
        read_config_boolean("FONCTIONAL", "autosort", "False")
        == "True"
    ):
        sort(openfile)


def deleteone(indextodelete, openfile=open):
    """
    Delete a task from the todofile
    """
    index_existant = False
    with openfile(todofilefromconfig(), "r") as todofile:
        lines = todofile.readlines()
    with openfile(todofilefromconfig(), "w") as todofile:
        for line in lines:
            # if the current row doesn't contain the index it is kept
            if not re.findall("^" + indextodelete + " ", line):
                todofile.write(line)
            # else it is deleted by not being copied
            else:
                printinfo(
                    "task deleted from the todolist - "
                    + line.rstrip("\n")
                )
                index_existant = True
    if not index_existant:
        printwarning(
            "no task is deleted from the todolist, not existing index - "
            + indextodelete
        )
