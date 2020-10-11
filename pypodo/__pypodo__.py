import os
import re
import sys
import time
from pathlib import Path
from shutil import copyfile

from termcolor import colored

STR_PATH_HOME__TODO_ = str(Path.home()) + '/.todo'
TAG_URGENT = "urgent"
STR_PATH_HOME__TODO_BACKUP_FOLDER_ = str(Path.home()) + '/.todo_backup/'


def help(open=open):
    if len(sys.argv) == 2:
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
    else:
        printerror("0 parameter is needed for pypodo help")


# list the .todo possibly filtered on the tags corresponding to the parameter


def list(open=open):
    check(open)

    vide = 'true'
    with open(STR_PATH_HOME__TODO_, 'r') as f:
        for line in f.readlines():
            # without filter -> we print all
            if len(sys.argv) == 2:
                vide = printlinetodo(line, vide)
            # with filter -> we check tag
            elif len(sys.argv) >= 3:
                display = 'true'
                for x in range(2, len(sys.argv)):
                    tag = sys.argv[x]
                    if not re.findall("#"+re.escape(tag)+"( |$)", line.rstrip('\n')):
                        display = 'false'
                # regex to search tags "#toto " or "#toto" at the end of the line
                if display == 'true':
                    vide = printlinetodo(line, vide)
    if vide == 'true':
        if len(sys.argv) >= 3:
            printwarning("the filtered todolist is empty")
        else:
            printwarning("the todolist is empty")


# list the .todo possibly filtered on the tags corresponding to the parameter
def listnotag(open=open):
    check(open)
    if len(sys.argv) > 2:
        printerror("0 parameter is needed for pypodo listnotag")
    else:
        vide = 'true'
        with open(STR_PATH_HOME__TODO_, 'r') as f:
            for line in f.readlines():
                if not '#' in line:
                    vide = printlinetodo(line, vide)
        if vide == 'true':
            printwarning("the filtered todolist with no tag is empty")

# list the .todo possibly filtered on the tags corresponding to the parameter


def listtag(open=open):
    check(open)
    if len(sys.argv) > 2:
        printerror("0 parameter is needed for pypodo listtag")
    else:
        vide = 'true'
        with open(STR_PATH_HOME__TODO_, 'r') as f:
            my_list = []
            for line in f.readlines():
                for part in line.split():
                    if "#" in part:
                        my_list.append(part)
                        vide = 'false'
            print(colored("\n".join(sorted(set(my_list))), "green"))
        if vide == 'true':
            printwarning("the filtered todolist with no tag is empty")


# adds the tasks as a parameter to the todolist (by calculating their indexes).
def add(open=open):
    check(open)
    if len(sys.argv) < 3:
        print("error : 1 or more parameter is needed for pypodo add - tasks")
    else:
        # loop on the indexes
        for x in range(2, len(sys.argv)):
            task = sys.argv[x]
            # check format : words* #tag1 #tag2 : task at free format, tags in one word prefixed by #
            if not re.findall("^([^# ])([^#])*( #[^ #]+)*$", task):
                printwarning("the task has not a valid format - "+task)
            else:
                with open(STR_PATH_HOME__TODO_, 'r') as f:
                    lines = f.readlines()
                # index calculation
                if len(lines) > 0:
                    last_line = lines[len(lines)-1]
                    index = int(last_line.split()[0])+1
                else:
                    index = 1
                # adding task to the todolist
                with open(STR_PATH_HOME__TODO_, 'a') as f:
                    f.write(str(index)+" "+task+'\n')
                    printinfo("task is added to the todolist - " +
                              str(index)+" "+task)

# removes the tasks whose indexes are provided as a parameter


def delete(open=open):
    check(open)
    if len(sys.argv) >= 3:
        # loop on the indexes
        for x in range(2, len(sys.argv)):
            index = sys.argv[x]
            # check the numeric format of the index
            if not re.findall("^\\d+$", index):
                printwarning(
                    "the index to delete is not in numeric format - " + index)
            else:
                index_existant = 'false'
                with open(STR_PATH_HOME__TODO_, 'r') as f:
                    lines = f.readlines()
                with open(STR_PATH_HOME__TODO_, 'w') as f:
                    for line in lines:
                        # if the current row doesn't contain the index it is kept
                        if not re.findall("^"+index+' ', line):
                            f.write(line)
                        # else it is deleted by not being copied
                        else:
                            printinfo(
                                "task deleted from the todolist - " + line.rstrip('\n'))
                            index_existant = 'true'
                if index_existant == 'false':
                    printwarning(
                        "no task is deleted from the todolist, not existing index - " + index)
    else:
        printerror(
            "1 or more parameter is needed for pypodo del - indexes to delete in numeric format")


# sort the list in successive ascending order
def sort(open=open):
    check(open)
    if len(sys.argv) != 2:
        printerror("0 parameter is needed for pypodo sort")
    else:
        vide = 'true'
        index = 1
        with open(STR_PATH_HOME__TODO_, 'r') as f:
            lines = f.readlines()
        with open(STR_PATH_HOME__TODO_, 'w') as f:
            for line in lines:
                # we replace the existing index by the current index that we increment
                replaced = re.sub("^\\d+ ", str(index)+" ", line)
                index = index+1
                f.write(replaced)
                vide = 'false'
        if vide == 'true':
            printwarning("the todolist is empty - nothing to do")
        else:
            printinfo("the todolist is sorted")
            list(open)

# various checks on the todo file


def check(open=open):
    file_exists = os.path.isfile(STR_PATH_HOME__TODO_)
    if file_exists:
        with open(STR_PATH_HOME__TODO_, 'r') as f:
            error = 'false'
            for line in f.readlines():
                # verification regex, index + task + possible tags
                if not re.findall("^\\d+ ([^#])+( #[^ #]+)*$", line.rstrip('\n')):
                    printwarning(
                        "this line has not a valid format in .todo - "+line.rstrip('\n'))
                    error = 'true'
        if error == 'true':
            printerror("verify the .todo file")
    else:
        open(STR_PATH_HOME__TODO_, "w")
        printinfo("creating .todolist file")

# untag tasks


def untag(open=open):
    check(open)
    if len(sys.argv) == 2:
        listnotag(open)
    elif len(sys.argv) >= 4:
        tag = sys.argv[2]
        if not re.findall("^[^ #]+$", tag):
            printerror("the tag has not a valid format - "+tag)
        # loop on the indexes
        for x in range(3, len(sys.argv)):
            index = sys.argv[x]
            if not re.findall("^\\d+$", index):
                printwarning(
                    "the index to untag is not in numeric format - " + index)
            else:
                index_trouve = 'false'
                with open(STR_PATH_HOME__TODO_, 'r') as f:
                    lines = f.readlines()
                with open(STR_PATH_HOME__TODO_, 'w') as f:
                    for line in lines:
                        if not re.findall("^"+index+' ', line):
                            f.write(line)
                        if re.findall("^"+index+' ', line):
                            if re.findall("#"+re.escape(tag)+'( |$)', line.rstrip('\n')):
                                f.write(re.sub("#"+re.escape(tag)+'( |$)',
                                               "", line).rstrip('\n').rstrip()+'\n')
                                printinfo("tag deleted from the task of the todolist - " + line.rstrip(
                                    '\n') + " -> " + re.sub("#"+re.escape(tag)+'( |$)', "", line.rstrip('\n')))
                            else:
                                f.write(line)
                                printwarning(
                                    "no tags is deleted from the todolist for the task - "+line.rstrip('\n'))
                            index_trouve = 'true'
                if index_trouve == 'false':
                    printwarning("no task with index - "+index)
    else:
        printerror(
            "1 parameter is needed for pypodo untag : the index of the task whose tags to delete")


# tagging task
def tag(open=open):
    check(open)
    if len(sys.argv) == 2:
        listtag(open)
    elif len(sys.argv) >= 4:
        tag = sys.argv[2]
        if not re.findall("^[^ #]+$", tag):
            printerror("the tag has not a valid format - "+tag)
        # loop on the indexes
        for x in range(3, len(sys.argv)):
            index = sys.argv[x]
            if not re.findall("^\\d+$", index):
                printwarning(
                    "the index to tag is not in numeric format - " + index)
            else:
                index_trouve = 'false'
                with open(STR_PATH_HOME__TODO_, 'r') as f:
                    lines = f.readlines()
                with open(STR_PATH_HOME__TODO_, 'w') as f:
                    for line in lines:
                        if not re.findall("^"+index+' ', line):
                            f.write(line)
                        if re.findall("^"+index+' ', line):
                            f.write(line.rstrip('\n')+" #"+tag+"\n")
                            printinfo("tag added to the task of the todolist - " +
                                      line.rstrip('\n') + " -> " + line.rstrip('\n')+" #"+tag)
                            index_trouve = 'true'
                if index_trouve == 'false':
                    printwarning(
                        "no task with number is in the todolist - "+index)
    else:
        printerror(
            "2 or more parameters are needed for pypodo tag : the tag to added and indexes of the task are in numeric format")


def backup(open=open):
    check(open)
    if len(sys.argv) > 2:
        printerror("0 parameter is needed for pypodo backup")
    else:
        dir_exists = os.path.exists(STR_PATH_HOME__TODO_BACKUP_FOLDER_)
        if not dir_exists:
            os.makedirs(STR_PATH_HOME__TODO_BACKUP_FOLDER_)
            printinfo("creating todolist backup folder")
        time_suffix = time.strftime("%Y%m%d%H%M%S")
        todobackupname = ".todo" + time_suffix
        backup_name = STR_PATH_HOME__TODO_BACKUP_FOLDER_ + todobackupname
        copyfile(STR_PATH_HOME__TODO_, backup_name)
        printinfo("creating todolist backup - " + todobackupname)

def find(open=open):
    check(open)
    if len(sys.argv) != 3:
        printerror("1 parameter is needed for pypodo find")
    else:
        vide = 'true'
        with open(STR_PATH_HOME__TODO_, 'r') as f:
            for line in f.readlines():
                search = sys.argv[2]
                if re.findall(search, line.rstrip('\n')):
                    vide = printlinetodo(line, vide)
        if vide == 'true':
            printwarning("the filtered todolist is empty")

def printlinetodo(line, vide):
    task = colored(
        re.sub("#.*", "", re.sub("^[^ ]+ ", "", line.rstrip('\n'))), "green")
    index = colored(line.split(' ', 1)[0], "blue")
    tags_nocolor = re.sub(
        "^[^#]+ #", "#", re.sub("^[^#]+$", "", re.sub("^[^ ]+ ", "", line.rstrip('\n'))))
    tags = re.sub(
        r"(#[^ #]+( |$)?)", colored(r"\1", "yellow"), tags_nocolor)
    tags = re.sub(r"33m#"+TAG_URGENT, "31m#"+TAG_URGENT, tags)
    print(index + " " + task + tags)
    vide = 'false'
    return vide


def printinfo(text):
    print(colored("info : " + text, "green"))


def printwarning(text):
    print(colored("warning : " + text, "yellow"))


def printerror(text):
    print(colored("error : " + text, "red"))


def sort_uniq(sequence):
    import itertools
    return (x[0] for x in itertools.groupby(sorted(sequence)))


def pypodo():
    import sys
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
    elif sys.argv[1] == "help":
        help()
    else:
        help()
