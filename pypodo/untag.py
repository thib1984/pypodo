"""
Pypodo scripts
"""


import re


from pypodo.properties import (
    REGEX_INDEX,
    REGEX_SPACE_OR_ENDLINE,
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
from pypodo.check import check



def untag(openfile=open):
    """
    Untag tasks from the todofile
    """
    if len(compute_args().untag) >= 2:
        tagtodel = compute_args().untag[0]
        if not re.findall("^[^ #]+$", tagtodel):
            printerror("the tag has not a valid format - " + tagtodel)
        else:
            # loop on the indexes
            for increment in range(1, len(compute_args().untag)):
                index = compute_args().untag[increment]
                # check the numeric format of the index
                if re.findall(REGEX_INDEX, index):
                    untagone(index, tagtodel, openfile)
                elif re.findall("^\\d+-\\d+$", index) and int(
                    index.split("-")[0]
                ) < int(index.split("-")[1]):
                    for indexlist in range(
                        int(index.split("-")[0]),
                        int(index.split("-")[1]) + 1,
                    ):
                        untagone(str(indexlist), tagtodel, openfile)
                else:
                    printwarning(
                        "the index to untag is not in numeric format - "
                        + index
                    )

    else:
        printerror(
            "2 or more parameters is needed for pypodo untag : the tag to delete and"
            " the indexes of the task whose tags to delete"
        )


def untagone(index, tagtodel, openfile):
    """
    Untag on task
    """
    index_trouve = False
    with openfile(todofilefromconfig(), "r") as todofile:
        lines = todofile.readlines()
    with openfile(todofilefromconfig(), "w") as todofile:
        for line in lines:
            if not re.findall("^" + index + " ", line):
                todofile.write(line)
            else:
                if re.findall(
                    " #"
                    + re.escape(tagtodel)
                    + REGEX_SPACE_OR_ENDLINE,
                    line.rstrip("\n"),
                ):
                    newline = re.sub(
                        "#"
                        + re.escape(tagtodel)
                        + REGEX_SPACE_OR_ENDLINE,
                        "",
                        line,
                    ).rstrip("\n")
                    todofile.write(newline.rstrip() + "\n")
                    printinfo(
                        "tag deleted from the task of the todolist - "
                        + line.rstrip("\n")
                        + " -> "
                        + newline.rstrip()
                    )
                else:
                    todofile.write(line)
                    printwarning(
                        "no tags is deleted from the todolist for the task - "
                        + line.rstrip("\n")
                    )
                index_trouve = True
    if not index_trouve:
        printwarning("no task with index - " + index)
