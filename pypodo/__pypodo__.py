"""
Pypodo scripts
"""

import os
import re
import sys
import time
from pathlib import Path
from shutil import copyfile
from datetime import datetime
from datetime import date
import configparser
from termcolor import colored

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
    if len(sys.argv) == 1:
        helppypodo()
    elif sys.argv[1] == "list":
        listtask(openfile)
    elif sys.argv[1] == "add":
        add(openfile)
    elif sys.argv[1] == "del":
        delete(openfile)
    elif sys.argv[1] == "sort":
        sort(openfile)
    elif sys.argv[1] == "help":
        helppypodo()
    elif sys.argv[1] == "untag":
        untag(openfile)
    elif sys.argv[1] == "tag":
        tag(openfile)
    elif sys.argv[1] == "backup":
        backup(openfile)
    elif sys.argv[1] == "find":
        find(openfile)
    else:
        helppypodo()


# primary functions
def helppypodo():
    """
    Display help message
    """
    help_txt = """\

    NAME
        pypodo

    SYNOPSIS
        pypodo is a todolist tool which works with a .todo file positionned the root of the home directory
        pypodo [MODE] [PARAMETERS]...

        help  : display this help
                -> pypodo help
        list  : display the todolist filtered on the tasks tagged with [PARAMETER]...
                -> pypodo list #print the full todolist
                -> pypodo list linux #display the todolist filtered on the task tagged with linux
                -> pypodo list linux urgent #display the todolist filtered on the task tagged with linux and urgent
        add   : add task(s) in [PARAMETER]... to the todolist with an index autogenerated
                -> pypodo add "my first task #linux" "my second task" #add the task "my first task #linux" (tag with linux) and the task "my second task" to the todolist
        del   : delete task(s) identified with the index equals to [PARAMETER]... from the todolist
                -> pypodo del 3 4 #delete the tasks identified by index equals 3 and 4	
        tag   : add the tag [PARAMETER[1]] to the task the task identified with the index equals to [PARAMETER[2]]... 
                or without parameters, display the tags of the todolist
                -> pypodo tag linux 3 4 #add the tag linux to the task identified with the index equals to 3 and 4
                -> pypodo tag	#display the tags of the todolist
        untag : delete the tag identidied by [PARAMETER1] in the task definied by the [PARAMETER2]... 
                or without parameter, display task without tags
                -> ypodo untag linux 3 4 #delete the tag linux from the tasks identified by index equals 3 and 4
                -> pypodo untag #display the todolist filtered on untagged tasks	
        sort  : reorder the todolist in consecutives index
                -> pypodo sort	#reorder the todolist in consecutives index	
        backup: create a timestamped copy of the actual .todo file in a backupfolder
                -> pypodo backup	#create a timestamped copy of the actual .todo file in a backupfolder	
        find  : filter the todo list on the paramter (regex accepted)
                -> pypodo filter "ta.*che"	#filter on the regex ta.*che	                             			
        """
    print(help_txt)


def listtask(openfile=open):
    """
    Print the todofile with filters or not
    """
    if check(openfile):

        empty = True
        with openfile(todofilefromconfig(), "r") as todofile:
            for line in todofile.readlines():
                # without filter -> we print all
                if len(sys.argv) == 2:
                    printlinetodo(line)
                    empty = False
                # with filter -> we check tag
                else:
                    display = True
                    for increment in range(2, len(sys.argv)):
                        tagtofilter = sys.argv[increment]
                        if not re.findall(
                            "#"
                            + re.escape(tagtofilter)
                            + REGEX_SPACE_OR_ENDLINE,
                            line.rstrip("\n"),
                        ):
                            display = False
                    # regex to search tags "#toto " or "#toto" at the end of the line
                    if display:
                        printlinetodo(line)
                        empty = False
        if empty:
            if len(sys.argv) >= 3:
                printwarning("the filtered todolist is empty")
            else:
                printwarning("the todolist is empty")


def add(openfile=open):
    """
    Add a task to the todofile
    """
    if check(openfile):
        if len(sys.argv) < 3:
            printerror(
                "1 or more parameter is needed for pypodo add - tasks"
            )
        else:
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
                for increment in range(2, len(sys.argv)):
                    task = sys.argv[increment]
                    # check format : words* #tag1 #tag2 : task at free format,
                    # tags in one word prefixed by #
                    if not re.findall(
                        "^([^# ])([^#])*( #[^ #]+)*$", task
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
    if check(openfile):
        if len(sys.argv) >= 3:
            # loop on the indexes
            for increment in range(2, len(sys.argv)):
                index = sys.argv[increment]
                # check the numeric format of the index

                if not re.findall(REGEX_INDEX, index):
                    printwarning(
                        "the index to delete is not in numeric format - "
                        + index
                    )
                else:
                    index_existant = False
                    with openfile(
                        todofilefromconfig(), "r"
                    ) as todofile:
                        lines = todofile.readlines()
                    with openfile(
                        todofilefromconfig(), "w"
                    ) as todofile:
                        for line in lines:
                            # if the current row doesn't contain the index it is kept
                            if not re.findall(
                                "^" + index + " ", line
                            ):
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
                            + index
                        )
            if (
                read_config_boolean("FONCTIONAL", "autosort", "False")
                == "True"
            ):
                sys.argv = [sys.argv[0]]
                sort(openfile)
        else:
            printerror(
                "1 or more parameter is needed for pypodo del - indexes to delete in numeric format"
            )


def sort(openfile=open):
    """
    Reorder the todofile with consecutives indexes
    """
    if check(openfile):
        if len(sys.argv) > 2:
            printerror("0 parameter is needed for pypodo sort")
        else:
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
    if check(openfile):
        if len(sys.argv) == 2:
            listnotag(openfile)
        elif len(sys.argv) >= 4:
            tagtodel = sys.argv[2]
            if not re.findall("^[^ #]+$", tagtodel):
                printerror(
                    "the tag has not a valid format - " + tagtodel
                )
            else:
                # loop on the indexes
                for increment in range(3, len(sys.argv)):
                    index = sys.argv[increment]
                    if not re.findall(REGEX_INDEX, index):
                        printwarning(
                            "the index to untag is not in numeric format - "
                            + index
                        )
                    else:
                        index_trouve = False
                        with openfile(
                            todofilefromconfig(), "r"
                        ) as todofile:
                            lines = todofile.readlines()
                        with openfile(
                            todofilefromconfig(), "w"
                        ) as todofile:
                            for line in lines:
                                if not re.findall(
                                    "^" + index + " ", line
                                ):
                                    todofile.write(line)
                                else:
                                    if re.findall(
                                        "#"
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
                                        todofile.write(
                                            newline.rstrip() + "\n"
                                        )
                                        printinfo(
                                            "tag deleted from the task of the todolist - "
                                            + line.rstrip("\n")
                                            + " -> "
                                            + newline
                                        )
                                    else:
                                        todofile.write(line)
                                        printwarning(
                                            "no tags is deleted from the todolist for the task - "
                                            + line.rstrip("\n")
                                        )
                                    index_trouve = True
                        if not index_trouve:
                            printwarning(
                                "no task with index - " + index
                            )
        else:
            printerror(
                "0,2 or more parameters is needed for pypodo untag : the tag to delete and"
                " the indexes of the task whose tags to delete - nothing to list task without tags"
            )


def tag(openfile=open):
    """
    Tag tasks from the todofile
    """
    if check(openfile):
        if len(sys.argv) == 2:
            listtag(openfile)
        elif len(sys.argv) >= 4:
            tagtoadd = sys.argv[2]
            if not re.findall("^[^ #]+$", tagtoadd):
                printerror(
                    "the tag has not a valid format - " + tagtoadd
                )
            else:
                # loop on the indexes
                for increment in range(3, len(sys.argv)):
                    index = sys.argv[increment]
                    if not re.findall(REGEX_INDEX, index):
                        printwarning(
                            "the index to tag is not in numeric format - "
                            + index
                        )
                    else:
                        index_trouve = False
                        with openfile(
                            todofilefromconfig(), "r"
                        ) as todofile:
                            lines = todofile.readlines()
                        with openfile(
                            todofilefromconfig(), "w"
                        ) as todofile:
                            for line in lines:
                                if not re.findall(
                                    "^" + index + " ", line
                                ):
                                    todofile.write(line)
                                else:
                                    newline = (
                                        line.rstrip("\n")
                                        + " #"
                                        + tagtoadd
                                    )
                                    todofile.write(newline + "\n")
                                    printinfo(
                                        "tag added to the task of the todolist - "
                                        + line.rstrip("\n")
                                        + " -> "
                                        + newline
                                    )
                                    index_trouve = True
                        if not index_trouve:
                            printwarning(
                                "no task with index - " + index
                            )
        else:
            printerror(
                "0,2 or more parameters is needed for pypodo tag : the tag to add and"
                " the indexes of the task whose tags to add - nothing to list tags of"
                " the todolist"
            )


def backup(openfile=open):
    """
    Backup the todofile
    """
    if check(openfile):
        if len(sys.argv) > 2:
            printerror("0 parameter is needed for pypodo backup")
        else:
            dir_exists = os.path.exists(todobackupfoderfromconfig())
            if not dir_exists:
                os.makedirs(todobackupfoderfromconfig())
                printinfo("creating todolist backup folder")
            time_suffix = time.strftime("%Y%m%d%H%M%S")
            todo_backup_name = ".todo" + time_suffix
            backup_name = (
                todobackupfoderfromconfig() + todo_backup_name
            )
            copyfile(todofilefromconfig(), backup_name)
            printinfo(
                "creating todolist backup - " + todo_backup_name
            )


def find(openfile=open):
    """
    Search with regex in the todofile
    """
    if check(openfile):
        if len(sys.argv) != 3:
            printerror("1 parameter is needed for pypodo find")
        else:
            empty = True
            with open(todofilefromconfig(), "r") as todofile:
                for line in todofile.readlines():
                    search = sys.argv[2]
                    if re.findall(search, line.rstrip("\n")):
                        printlinetodo(line)
                        empty = False
            if empty:
                printwarning("the filtered todolist is empty")


# secondary functions
def listnotag(openfile=open):
    """
    Print the todofile filtered on tasks with not tags
    """
    if check(openfile):
        if len(sys.argv) > 2:
            printerror("0 parameter is needed for pypodo listnotag")
        else:
            empty = True
            with openfile(todofilefromconfig(), "r") as todofile:
                for line in todofile.readlines():
                    if not "#" in line:
                        printlinetodo(line)
                        empty = False
            if empty:
                printwarning(
                    "the filtered todolist with no tag is empty"
                )


def listtag(openfile=open):
    """
    Print the tags of the todofile
    """
    if check(openfile):
        if len(sys.argv) > 2:
            printerror("0 parameter is needed for pypodo listtag")
        else:
            empty = True
            with openfile(todofilefromconfig(), "r") as todofile:
                my_list = []
                for line in todofile.readlines():
                    for part in line.split():
                        if "#" in part:
                            if part in listalerttags():
                                part = colored(part, color_alert())
                            elif test_date(part[1:]) == "alert":
                                part = colored(part, color_alert())
                            elif test_date(part[1:]) == "warning":
                                part = colored(part, color_warning())
                            else:
                                part = colored(part, color_tag())
                            my_list.append(part)
                            empty = False
            if empty:
                printwarning("the list of todolist's tags is empty")
            else:
                print("\n".join(sorted(set(my_list))))


def check(openfile=open):
    """
    Check the toodofile
    """
    file_exists = os.path.isfile(todofilefromconfig())
    if file_exists:
        with openfile(todofilefromconfig(), "r") as todofile:
            error = False
            for line in todofile.readlines():
                # verification regex, index + task + possible tags
                if not re.findall(
                    "^\\d+ ([^#])+( #[^ #]+)*$", line.rstrip("\n")
                ):
                    printwarning(
                        "this line has not a valid format in .todo - "
                        + line.rstrip("\n")
                    )
                    error = True
        if error:
            printerror("verify the .todo file")
            return False
        return True

    printinfo("creating .todolist file")
    openfile(todofilefromconfig(), "a")
    return True


# others functions
def todofilefromconfig():
    """
    Obtain path to todofile
    """
    return read_config(
        "SYSTEM", "todofile", str(Path.home()) + "/.todo"
    )


def todobackupfoderfromconfig():
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
    task = colored(
        re.sub(" #.*", "", re.sub("^[^ ]+ ", "", line.rstrip("\n"))),
        color_task(),
    )
    index = colored(line.split(" ", 1)[0], color_index())
    tags = ""
    for part in line.split():
        if "#" in part:
            if part in listalerttags():
                tags = tags + " " + (colored(part, color_alert()))
            elif test_date(part[1:]) == "alert":
                tags = tags + " " + (colored(part, color_alert()))
            elif test_date(part[1:]) == "warning":
                tags = tags + " " + (colored(part, color_warning()))
            else:
                tags = tags + " " + (colored(part, color_tag()))
    print(index + " " + task + tags)


def printinfo(text):
    """
    Color and key word info for print
    """
    if read_config_level("SYSTEM", "messagelevel", "info") == "info":
        print(colored("info    : " + text, color_info()))


def printwarning(text):
    """
    Color and key word warning for print
    """
    if (
        read_config_level("SYSTEM", "messagelevel", "info") == "info"
        or read_config_level("SYSTEM", "messagelevel", "info")
        == "warning"
    ):
        print(colored("warning : " + text, color_warning()))


def printerror(text):
    """
    Color and key word error for print
    """
    print(colored("error   : " + text, color_alert()))


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
def read_config(section, cle, defaut):
    """
    Read the config file
    """
    config = configparser.ConfigParser()
    try:
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
    if level not in ["warning", "info", "error"]:
        return defaut
    return level


def test_date(datetime_str):
    """
    Comparare date en return alert state
    """
    try:
        datetime_object = datetime.strptime(
            datetime_str, "%Y%m%d"
        ).date()
    except ValueError:
        return "ok"
    if (date.today() - datetime_object).days >= -1 * periodalert():
        return "alert"
    if (date.today() - datetime_object).days >= -1 * periodwarning():
        return "warning"
    return "ok"
