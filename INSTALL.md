# Prerequisites

- Install Python 3 for your system
- Install pip3* for your system

# Install/Upgrade/Uninstall

- ``pip3 install pypodo``* to install
- ``pypodo --update`` or ``pip3 install --upgrade``* to upgrade
- ``pip3 uninstall pypodo``* to uninstall

*_Use pip instead of pip3, if pip3 does not exist_
# Configuration [optional]

You can customize the application with the ``~/.todo.rc`` file. Create it if it does not exist and copy paste this content. The autosort option runs a pypodo sort after pypodo del.

```
####grey,red,green,yellow,blue,magenta,cyan,white only ;)
[COLOR]
#alert = red
#warning = yellow
#info = green
#index = blue
#task = green
#tag = cyan
#debug = grey

[SYSTEM]
####debug,info,warning,error
#messagelevel = info
####format double % character, use for warning and alert on dates
#formatdate = %%Y%%m%%d
#todofile = ~/.todo
#todobackupfolder = ~/.todo_backup/


[FONCTIONAL]
####int values
#periodalert = 0
#periodwarning = 7
####tags with '#' and with a coma separation
#alerttags = #urgent
####True to autosort todolist
#autosort = False
```
# Use with newsboat [optional]

If you use [newsboat](https://github.com/newsboat/newsboat), you can modify the configuration of the rss reader to save url of your favorites articles with 'o' press.

```
browser "pypodo add '%u #rss'"
```

# File sharing [optional]

You can use the .todo.rc configuration file to change the path of your todofile. If you used a "cloud folder" as cozy drive, you can share your pypodo app between two or more computeurs!

