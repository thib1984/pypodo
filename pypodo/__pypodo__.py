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

STR_PATH_HOME__TODO_ = str(Path.home()) + '/.todo'
STR_PATH_HOME__TODORC_ = str(Path.home()) + '/.todo.rc'
TAG_URGENT = "urgent"
STR_PATH_HOME__TODO_BACKUP_FOLDER_ = str(Path.home()) + '/.todo_backup/'
REGEX_INDEX = "^\\d+$"
REGEX_SPACE_OR_ENDLINE = "( |$)"
RED = "33m#"
YELLOW = "31m#"


def help():
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
                pypodo help
        list  : print the todolist with an index for each task, with tag filtered on [PARAMETER]
                pypodo list #print the todolist
                pypodo list linux #print the todolist filtered on tag linux
        add   : add [PARAMETER]... to the todolist with an index autogenerated
                pypodo add "my first task" "my second task" #add the task "my first task" and the task "my second task" to the todolist
        del   : delete task(s) identified with the index equals to [PARAMETER]... from the todolis
                pypodo del 3 4 #deletes the task identified by index equals 3 and 4	
        tag   : add the tag [PARAMETER[1]] to the task the task identified with the index equals to [PARAMETER[2]]... or without parameters, display the tags of the todolist
                pypodo tag linux 3 4 #add the tag linux to the task identified with the index equals to 3 and 4
                pypodo tag	#print the tags of the todolist
        untag : delete the tag identidied by [PARAMETER1] in the task definied by the [PARAMETER2]... or without parameter, display task without tags
                pypodo untag linux 3 4 #delete the tag linux from the task identified by index equals 3 and 4
                pypodo untag #print the todolist filtered on untagged tasks	
        sort  : reorder the todolist in consecutives index
                pypodo sort	#reorder the todolist in consecutives index	
        backup  : create a timestamped copy of the actual .todo file in a backupfolder
                pypodo backup	#create a timestamped copy of the actual .todo file in a backupfolder	 
        find  : filter the todo list on the paramter (regex accepted)
                pypodo filter "ta.*che"	#filter on the regex ta.*che	                             			
        """
    print(help_txt)


def list(open=open):
    """
    Print the todofile with filters or not
    """
    if check(open):

        empty = True
        with open(STR_PATH_HOME__TODO_, 'r') as todofile:
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
                        if not re.findall("#"+re.escape(tagtofilter)+REGEX_SPACE_OR_ENDLINE, line.rstrip('\n')):
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


def listnotag(open=open):
    """
    Print the todofile filtered on tasks with not tags
    """
    if check(open):
        if len(sys.argv) > 2:
            printerror("0 parameter is needed for pypodo listnotag")
        else:
            empty = True
            with open(STR_PATH_HOME__TODO_, 'r') as todofile:
                for line in todofile.readlines():
                    if not '#' in line:
                        printlinetodo(line)
                        empty = False
            if empty:
                printwarning("the filtered todolist with no tag is empty")


def listtag(open=open):
    """
    Print the tags of the todofile
    """
    if check(open):
        if len(sys.argv) > 2:
            printerror("0 parameter is needed for pypodo listtag")
        else:
            empty = True
            with open(STR_PATH_HOME__TODO_, 'r') as todofile:
                my_list = []
                for line in todofile.readlines():
                    for part in line.split():
                        if "#" in part:
                            if part == "#urgent":
                                part = colored(part, color_alert())
                            elif test_date(part[1:]) == "alert":
                                part = colored(part, color_alert())
                            elif test_date(part[1:]) == "warning":
                                part = colored(part, color_warning())
                            else:
                                part = colored(part, color_tag())
                            my_list.append(part)
                            empty = False
                print("\n".join(sorted(set(my_list))))
            if empty:
                printwarning("the filtered todolist with no tag is empty")


def add(open=open):
    """
    Add a task to the todofile
    """
    if check(open):
        if len(sys.argv) < 3:
            printerror("1 or more parameter is needed for pypodo add - tasks")
        else:
            # loop on the indexes
            for increment in range(2, len(sys.argv)):
                task = sys.argv[increment]
                # check format : words* #tag1 #tag2 : task at free format, tags in one word prefixed by #
                if not re.findall("^([^# ])([^#])*( #[^ #]+)*$", task):
                    printwarning("the task has not a valid format - "+task)
                else:
                    with open(STR_PATH_HOME__TODO_, 'r') as todofile:
                        lines = todofile.readlines()
                    # index calculation
                    if len(lines) > 0:
                        last_line = lines[len(lines)-1]
                        index = int(last_line.split()[0])+1
                    else:
                        index = 1
                    # adding task to the todolist
                    with open(STR_PATH_HOME__TODO_, 'a') as todofile:
                        todofile.write(str(index)+" "+task+'\n')
                        printinfo("task is added to the todolist - " +
                                  str(index)+" "+task)


def delete(open=open):
    """
    Delete a task from the todofile
    """
    if check(open):
        if len(sys.argv) >= 3:
            # loop on the indexes
            for increment in range(2, len(sys.argv)):
                index = sys.argv[increment]
                # check the numeric format of the index

                if not re.findall(REGEX_INDEX, index):
                    printwarning(
                        "the index to delete is not in numeric format - " + index)
                else:
                    index_existant = False
                    with open(STR_PATH_HOME__TODO_, 'r') as todofile:
                        lines = todofile.readlines()
                    with open(STR_PATH_HOME__TODO_, 'w') as todofile:
                        for line in lines:
                            # if the current row doesn't contain the index it is kept
                            if not re.findall("^"+index+' ', line):
                                todofile.write(line)
                            # else it is deleted by not being copied
                            else:
                                printinfo(
                                    "task deleted from the todolist - " + line.rstrip('\n'))
                                index_existant = True
                    if not index_existant:
                        printwarning(
                            "no task is deleted from the todolist, not existing index - " + index)
        else:
            printerror(
                "1 or more parameter is needed for pypodo del - indexes to delete in numeric format")


def sort(open=open):
    """
    Reorder the todofile with consecutives indexes
    """
    if check(open):
        if len(sys.argv) != 2:
            printerror("0 parameter is needed for pypodo sort")
        else:
            empty = True
            index = 1
            with open(STR_PATH_HOME__TODO_, 'r') as todofile:
                lines = todofile.readlines()
            with open(STR_PATH_HOME__TODO_, 'w') as todofile:
                for line in lines:
                    # we replace the existing index by the current index that we increment
                    replaced = re.sub("^\\d+ ", str(index)+" ", line)
                    index = index+1
                    todofile.write(replaced)
                    empty = False
            if empty:
                printwarning("the todolist is empty - nothing to do")
            else:
                printinfo("the todolist is sorted")
                list(open)


def check(open=open):
    """
    Check the toodofile
    """
    file_exists = os.path.isfile(STR_PATH_HOME__TODO_)
    if file_exists:
        with open(STR_PATH_HOME__TODO_, 'r') as todofile:
            error = False
            for line in todofile.readlines():
                # verification regex, index + task + possible tags
                if not re.findall("^\\d+ ([^#])+( #[^ #]+)*$", line.rstrip('\n')):
                    printwarning(
                        "this line has not a valid format in .todo - "+line.rstrip('\n'))
                    error = True
        if error:
            printerror("verify the .todo file")
            return False
        return True

    printinfo("creating .todolist file")
    open(STR_PATH_HOME__TODO_, "a")
    return True


def untag(open=open):
    """
    Untag tasks from the todofile
    """
    if check(open):
        if len(sys.argv) == 2:
            listnotag(open)
        elif len(sys.argv) >= 4:
            tagtodel = sys.argv[2]
            if not re.findall("^[^ #]+$", tagtodel):
                printerror("the tag has not a valid format - "+tagtodel)
            # loop on the indexes
            for increment in range(3, len(sys.argv)):
                index = sys.argv[increment]
                if not re.findall(REGEX_INDEX, index):
                    printwarning(
                        "the index to untag is not in numeric format - " + index)
                else:
                    index_trouve = False
                    with open(STR_PATH_HOME__TODO_, 'r') as todofile:
                        lines = todofile.readlines()
                    with open(STR_PATH_HOME__TODO_, 'w') as todofile:
                        for line in lines:
                            if not re.findall("^"+index+' ', line):
                                todofile.write(line)
                            else:
                                if re.findall("#"+re.escape(tagtodel)+REGEX_SPACE_OR_ENDLINE, line.rstrip('\n')):
                                    todofile.write(re.sub("#"+re.escape(tagtodel)+REGEX_SPACE_OR_ENDLINE,
                                                          "", line).rstrip('\n').rstrip()+'\n')
                                    printinfo("tag deleted from the task of the todolist - " + line.rstrip(
                                        '\n') + " -> " + re.sub("#"+re.escape(tagtodel)+REGEX_SPACE_OR_ENDLINE, "", line.rstrip('\n')))
                                else:
                                    todofile.write(line)
                                    printwarning(
                                        "no tags is deleted from the todolist for the task - "+line.rstrip('\n'))
                                index_trouve = True
                    if not index_trouve:
                        printwarning("no task with index - "+index)
        else:
            printerror(
                "0,2 or more parameters is needed for pypodo untag : the tag to delete and the indexes of the task whose tags to delete - nothing to list task without tags")


def tag(open=open):
    """
    Tag tasks from the todofile
    """
    if check(open):
        if len(sys.argv) == 2:
            listtag(open)
        elif len(sys.argv) >= 4:
            tagtoadd = sys.argv[2]
            if not re.findall("^[^ #]+$", tagtoadd):
                printerror("the tag has not a valid format - "+tagtoadd)
            # loop on the indexes
            for increment in range(3, len(sys.argv)):
                index = sys.argv[increment]
                if not re.findall(REGEX_INDEX, index):
                    printwarning(
                        "the index to tag is not in numeric format - " + index)
                else:
                    index_trouve = False
                    with open(STR_PATH_HOME__TODO_, 'r') as todofile:
                        lines = todofile.readlines()
                    with open(STR_PATH_HOME__TODO_, 'w') as todofile:
                        for line in lines:
                            if not re.findall("^"+index+' ', line):
                                todofile.write(line)
                            else:
                                todofile.write(line.rstrip(
                                    '\n')+" #"+tagtoadd+"\n")
                                printinfo("tag added to the task of the todolist - " +
                                          line.rstrip('\n') + " -> " + line.rstrip('\n')+" #"+tagtoadd)
                                index_trouve = True
                    if not index_trouve:
                        printwarning(
                            "no task with number is in the todolist - "+index)
        else:
            printerror(
                "0,2 or more parameters is needed for pypodo tag : the tag to add and the indexes of the task whose tags to add - nothing to list tags of the todolist")


def backup(open=open):
    """
    Backup the todofile
    """
    if check(open):
        if len(sys.argv) > 2:
            printerror("0 parameter is needed for pypodo backup")
        else:
            dir_exists = os.path.exists(STR_PATH_HOME__TODO_BACKUP_FOLDER_)
            if not dir_exists:
                os.makedirs(STR_PATH_HOME__TODO_BACKUP_FOLDER_)
                printinfo("creating todolist backup folder")
            time_suffix = time.strftime("%Y%m%d%H%M%S")
            todo_backup_name = ".todo" + time_suffix
            backup_name = STR_PATH_HOME__TODO_BACKUP_FOLDER_ + todo_backup_name
            copyfile(STR_PATH_HOME__TODO_, backup_name)
            printinfo("creating todolist backup - " + todo_backup_name)


def find(open=open):
    """
    Search with regex in the todofile
    """
    if check(open):
        if len(sys.argv) != 3:
            printerror("1 parameter is needed for pypodo find")
        else:
            empty = True
            with open(STR_PATH_HOME__TODO_, 'r') as todofile:
                for line in todofile.readlines():
                    search = sys.argv[2]
                    if re.findall(search, line.rstrip('\n')):
                        printlinetodo(line)
                        empty = False
            if empty:
                printwarning("the filtered todolist is empty")


def test_date(datetime_str):
    """
    Comparare date en return alert state
    """
    try:
        datetime_object = datetime.strptime(datetime_str, '%Y%m%d').date()
    except ValueError:
        return "ok"
    if (date.today() - datetime_object).days >= 0:
        return "alert"
    if (date.today() - datetime_object).days >= -7:
        return "warning"
    return "ok"


def printlinetodo(line):
    """
    Display task with colors
    """
    task = colored(
        re.sub(" #.*", "", re.sub("^[^ ]+ ", "", line.rstrip('\n'))), color_task())
    index = colored(line.split(' ', 1)[0], color_index())
    tags = ""
    for part in line.split():
        if "#" in part:
            if part == "#urgent":
                tags = tags+" "+(colored(part, color_alert()))
            elif test_date(part[1:]) == "alert":
                tags = tags+" "+(colored(part, color_alert()))
            elif test_date(part[1:]) == "warning":
                tags = tags+" "+(colored(part, color_warning()))
            else:
                tags = tags+" "+(colored(part, color_tag()))
    print(index + " " + task + tags)


def printinfo(text):
    """
    Color and key word info for print
    """
    print(colored("info    : " + text, color_info()))


def printwarning(text):
    """
    Color and key word warning for print
    """
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
    return read_config("COLOR", "info", "green")


def color_task():
    """
    Color for task
    """
    return read_config("COLOR", "task", "green")


def color_index():
    """
    Color for index
    """
    return read_config("COLOR", "index", "yellow")


def color_tag():
    """
    Color for tag
    """
    return read_config("COLOR", "tag", "cyan")


def color_warning():
    """
    Color for warning
    """
    return read_config("COLOR", "warning", "yellow")


def color_alert():
    """
    Color for alert
    """
    return read_config("COLOR", "alert", "red")


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
    


def pypodo():
    """
    Entrypoint
    """
    if len(sys.argv) == 1:
        help()
    elif sys.argv[1] == "list":
        list()
    elif sys.argv[1] == "add":
        add()
    elif sys.argv[1] == "del":
        delete()
    elif sys.argv[1] == "sort":
        sort()
    elif sys.argv[1] == "help":
        help()
    elif sys.argv[1] == "untag":
        untag()
    elif sys.argv[1] == "tag":
        tag()
    elif sys.argv[1] == "backup":
        backup()
    elif sys.argv[1] == "find":
        find()
    else:
        help()
