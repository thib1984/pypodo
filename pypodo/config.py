from datetime import datetime
from datetime import date
import configparser
from os import sys
from pypodo.properties import (
    STR_PATH_HOME__TODORC_,
)
from termcolor import colored
from pypodo.args import compute_args
from pathlib import Path

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


def my_colored(text, color):
    if not compute_args().nocolor:
        return colored(text, color)
    return text


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
