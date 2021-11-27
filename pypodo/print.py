from pypodo.config import (
    read_config_color,
    read_config_level,
    my_colored,
    listalerttags,
    test_date,
)
from pypodo.args import compute_args
import re

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
    isalert= False
    iswarning= False
    for part in line.split():
        if part.startswith("#"):
            if part in listalerttags():
                isalert = True
            elif test_date(part[1:]) == "alert":
                isalert = True
            elif test_date(part[1:]) == "warning":
                iswarning = True     
            tags = tags + " " + part
    if isalert:
        tags= my_colored(tags, color_alert())
    elif iswarning:
        tags= my_colored(tags, color_warning())
    else:
        tags = my_colored(tags, color_tag())         
    return [index,task,tags]


def printdebug(text):
    """
    Color and key word debug for print
    """
    if (
        read_config_level("SYSTEM", "messagelevel", "info") == "debug"
        or compute_args().verbose
    ):
        print(my_colored("debug   : " + text, color_debug()))


def printinfo(text):
    """
    Color and key word info for print
    """
    if (
        read_config_level("SYSTEM", "messagelevel", "info") == "info"
        or read_config_level("SYSTEM", "messagelevel", "info")
        == "debug"
        or compute_args().verbose
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
        == "warning"
        or compute_args().verbose
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
