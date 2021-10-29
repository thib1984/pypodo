"""
Pypodo scripts
"""

import argparse
import os
import re
import sys
import time
import base64
import hashlib
from pathlib import Path
from shutil import copyfile
from datetime import datetime
from datetime import date
import configparser
from termcolor import colored
from pypodo.args import compute_args
STR_PATH_HOME__TODORC_ = str(Path.home()) + "/.todo.rc"
REGEX_INDEX = "^\\d+$"
REGEX_SPACE_OR_ENDLINE = "( |$)"
RED = "33m#"
YELLOW = "31m#"

# entrypoint
def pypodo(openfile=open):
    """
    Entrypoint
    """
    compute_args()
    if check(openfile):
        if compute_args().filter:
            listtask(openfile)
        elif compute_args().add:
            add(openfile)
        elif compute_args().delete:
            delete(openfile)
        elif compute_args().order:
            sort(openfile)
        elif compute_args().untag:
            untag(openfile)
        elif compute_args().tag:
            tag(openfile)
        elif compute_args().backup:
            backup(openfile)
        elif compute_args().search:
            find(openfile)
        else:
            listtask(openfile)       



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
            if not re.findall(
                "^([^#]|([^ ]#))*( #[^ #]+)*$", task
            ):
                printwarning(
                    "the task has not a valid format - "
                    + task
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
            replaced = re.sub(
                "^\\d+ ", str(index) + " ", line
            )
            index = index + 1
            todofile.write(replaced)
            empty = False
    if empty:
        printwarning("the todolist is empty - nothing to do")
    else:
        printinfo("the todolist is sorted")
        listtask(openfile)


def untag(openfile=open):
    """
    Untag tasks from the todofile
    """
    if len(compute_args().untag) >= 2:
        tagtodel = compute_args().untag[0]
        if not re.findall("^[^ #]+$", tagtodel):
            printerror(
                "the tag has not a valid format - " + tagtodel
            )
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
                        untagone(
                            str(indexlist), tagtodel, openfile
                        )
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


def tag(openfile=open):
    """
    Tag tasks from the todofile
    """
    if len(compute_args().tag) >= 2:
        tagtoadd = compute_args().tag[0]
        if not re.findall("^[^ #]+$", tagtoadd):
            printerror(
                "the tag has not a valid format - " + tagtoadd
            )
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


def backup(openfile=open):
    """
    Backup the todofile
    """
    dir_exists = os.path.exists(todobackupfolderfromconfig())
    if not dir_exists:
        try:
            os.makedirs(todobackupfolderfromconfig())
        except PermissionError:
            printerror(
                "permission error to create the backup folder : "
                + todobackupfolderfromconfig()
            )
            sys.exit()
        printinfo("creating todolist backup folder")
    time_suffix = time.strftime("%Y%m%d%H%M%S")
    todo_backup_name = ".todo" + time_suffix
    backup_name = (
        todobackupfolderfromconfig() + todo_backup_name
    )
    try:
        copyfile(todofilefromconfig(), backup_name)
    except PermissionError:
        printerror(
            "permission error to create the backup folder : "
            + todobackupfolderfromconfig()
        )
        sys.exit()
    printinfo(
        "creating todolist backup - " + todo_backup_name
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


def check(openfile=open):
    """
    Check the toodofile
    """
    file_exists = os.path.isfile(todofilefromconfig())
    if file_exists:
        try:
            with openfile(todofilefromconfig(), "r") as todofile:
                error = False
                for line in todofile.readlines():
                    # verification regex, index + task + possible tags
                    if not re.findall(
                        "^\\d+ ([^#]|([^ ]#))*( #[^ #]+)*$",
                        line.rstrip("\n"),
                    ):
                        printwarning(
                            "this line has not a valid format in .todo - "
                            + line.rstrip("\n")
                        )
                        error = True
            if error:
                printerror("verify the .todo file.")
                sys.exit()
            return True
        except PermissionError:
            printerror(
                "permission error to open the todofile : "
                + todofilefromconfig()
            )
            sys.exit()

    printinfo("creating .todolist file")
    try:
        f = openfile(todofilefromconfig(), "a")
        f.close
    except FileNotFoundError:
        printerror(
            "the path "
            + todofilefromconfig()
            + " does not exist, correct it (in the .todo.rc file)"
        )
        sys.exit()
    return True


# others functions
def todofilefromconfig():
    """
    Obtain path to todofile
    """
    return read_config(
        "SYSTEM", "todofile", str(Path.home()) + "/.todo"
    )


def todobackupfolderfromconfig():
    """
    Obtain path to todobackupfolder
    """
    return read_config(
        "SYSTEM",
        "todobackupfolder",
        str(Path.home()) + "/.todo_backup/",
    )


def periodalert():
    """
    Obtain period alert
    """
    return int(read_config_int("FONCTIONAL", "periodalert", "0"))


def periodwarning():
    """
    Obtain period warnning
    """
    return int(read_config_int("FONCTIONAL", "periodwarning", "7"))


def listalerttags():
    """
    Obtain list of alert tags
    """
    return read_config("FONCTIONAL", "alerttags", "#urgent").split(
        ","
    )


# print functions
def printlinetodo(line):
    """
    Display task with colors
    """
    task = my_colored(
        re.sub(" #.*", "", re.sub("^[^ ]+ ", "", line.rstrip("\n"))),
        color_task(),
    )
    index = my_colored(line.split(" ", 1)[0], color_index())
    tags = ""
    for part in line.split():
        if part.startswith("#"):
            if part in listalerttags():
                tags = tags + " " + (my_colored(part, color_alert()))
            elif test_date(part[1:]) == "alert":
                tags = tags + " " + (my_colored(part, color_alert()))
            elif test_date(part[1:]) == "warning":
                tags = tags + " " + (my_colored(part, color_warning()))
            else:
                tags = tags + " " + (my_colored(part, color_tag()))
    print(index + " " + task + tags)


def printdebug(text):
    """
    Color and key word debug for print
    """
    if read_config_level("SYSTEM", "messagelevel", "info") == "debug" or compute_args().verbose:
        print(my_colored("debug   : " + text, color_debug()))


def printinfo(text):
    """
    Color and key word info for print
    """
    if (
        read_config_level("SYSTEM", "messagelevel", "info") == "info"
        or read_config_level("SYSTEM", "messagelevel", "info")
        == "debug" or compute_args().verbose
    ):
        print(my_colored("info    : " + text, color_info()))


def printwarning(text):
    """
    Color and key word warning for print
    """
    if (
        read_config_level("SYSTEM", "messagelevel", "info") == "info"
        or read_config_level("SYSTEM", "messagelevel", "info")
        == "debug"
        or read_config_level("SYSTEM", "messagelevel", "info")
        == "warning" or compute_args().verbose
    ):
        print(my_colored("warning : " + text, color_warning()))


def printerror(text):
    """
    Color and key word error for print
    """
    print(my_colored("error   : " + text, color_alert()))


def color_debug():
    """
    Color for info
    """
    return read_config_color("COLOR", "debug", "grey")


def color_info():
    """
    Color for info
    """
    return read_config_color("COLOR", "info", "green")


def color_task():
    """
    Color for task
    """
    return read_config_color("COLOR", "task", "green")


def color_index():
    """
    Color for index
    """
    return read_config_color("COLOR", "index", "yellow")


def color_tag():
    """
    Color for tag
    """
    return read_config_color("COLOR", "tag", "cyan")


def color_warning():
    """
    Color for warning
    """
    return read_config_color("COLOR", "warning", "yellow")


def color_alert():
    """
    Color for alert
    """
    return read_config_color("COLOR", "alert", "red")


# config functions
def read_config(section, cle, defaut, openfile=open):
    """
    Read the config file
    """
    config = configparser.ConfigParser()
    try:
        try:
            try:
                f = openfile(STR_PATH_HOME__TODORC_, "r")
                f.close()
            except PermissionError:
                print(
                    my_colored(
                        "error   : permission error to open the ~/todo.rc file",
                        "red",
                    )
                )
                sys.exit()
        except FileNotFoundError:
            f = openfile(STR_PATH_HOME__TODORC_, "w")
            f.close()
        config.read(STR_PATH_HOME__TODORC_)
        return config[section][cle]
    except (configparser.MissingSectionHeaderError, KeyError):
        return defaut


def read_config_color(section, cle, defaut):
    """
    Read the config file for color
    """
    color = read_config(section, cle, defaut)
    if color not in [
        "grey",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
    ]:
        return defaut
    return color


def read_config_int(section, cle, defaut):
    """
    Read the config file for natural number
    """
    number = read_config(section, cle, defaut)
    if not number.isdigit():
        return defaut
    return number


def read_config_boolean(section, cle, defaut):
    """
    Read the config file for color
    """
    myboool = read_config(section, cle, defaut)
    if myboool not in ["True", "False"]:
        return defaut
    return myboool


def read_config_level(section, cle, defaut):
    """
    Read the config file for level
    """
    level = read_config(section, cle, defaut)
    if level not in ["warning", "info", "error", "debug"]:
        return defaut
    return level


def read_config_date_format(section, cle, defaut):
    """
    Read the config file for date format
    """
    return read_config(section, cle, defaut)


def test_date(datetime_str):
    """
    Comparare date en return alert state
    """
    try:
        datetime_object = datetime.strptime(
            datetime_str,
            read_config_date_format("SYSTEM", "formatdate", "%Y%m%d"),
        ).date()
    except ValueError:
        return "ok"
    if (date.today() - datetime_object).days >= -1 * periodalert():
        return "alert"
    if (date.today() - datetime_object).days >= -1 * periodwarning():
        return "warning"
    return "ok"


def my_colored(text,color):
    if not compute_args().nocolor:
        return colored(text,color)
    return text    