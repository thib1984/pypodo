"""
Pypodo scripts
"""

import re
from columnar import columnar
from pypodo.properties import (
    REGEX_SPACE_OR_ENDLINE,
)
from pypodo.config import (
    read_config_boolean,
    todofilefromconfig,
)
from pypodo.args import compute_args
from pypodo.print import (
    printwarning,
    printlinetodo,
    listalerttags,
    test_date,
)


def listtask(openfile=open):
    """
    Print the todofile with filters or not
    """
    empty = True
    headers = ["index", "task", "tags"]
    data = []
    with openfile(todofilefromconfig(), "r") as todofile:
        for line in todofile.readlines():
            # without filter -> we print all
            display = True
            if compute_args().filter:
                for tagtofilter in compute_args().filter:
                    # regex to search tags "#toto " or "#toto" at the end of the line
                    if not re.findall(
                        " #"
                        + re.escape(tagtofilter)
                        + REGEX_SPACE_OR_ENDLINE,
                        line.rstrip("\n"),
                    ):
                        display = False
            if compute_args().exclude:
                for tagtoexclude in compute_args().exclude:
                    # regex to search tags "#toto " or "#toto" at the end of the line
                    if re.findall(
                        " #"
                        + re.escape(tagtoexclude)
                        + REGEX_SPACE_OR_ENDLINE,
                        line.rstrip("\n"),
                    ):
                        display = False
            if compute_args().warning:
                isalert = False
                for part in line.split():
                    if (
                        part.startswith("#")
                        and part in listalerttags()
                        or test_date(part[1:]) == "alert"
                        or test_date(part[1:]) == "warning"
                    ):
                        isalert = True
                if isalert == False:
                    display = False
            if display:
                data.append(printlinetodo(line))
                empty = False
    if empty:
        if compute_args().filter:
            printwarning("the filtered todolist is empty")
        else:
            printwarning("the todolist is empty")
    else:
        if compute_args().condensate:
            table = columnar(data, no_borders=True, wrap_max=0)
        else:
            if (
                read_config_boolean(
                    "FONCTIONAL", "condensate", "False"
                )
                == "True"
            ):
                table = columnar(data, no_borders=True, wrap_max=0)
            else:
                table = columnar(
                    data, headers, no_borders=False, wrap_max=0
                )
        print(table)
