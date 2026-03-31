# Prerequisites

- Install Python 3 on your system
- Install pipx on your system
- Install git on your system

# Why use pipx?

`pipx` installs Python applications in isolated environments, which prevents dependency conflicts with your system or other projects.  
It also allows you to run CLI tools globally without polluting your Python installation.  
This makes it safer and cleaner than using `pip` or `pip3` for installing standalone tools.

# Clean old versions

If you have installed an old version with `pip` or `pip3` (depending on your system), use one of the following commands:

```
pip3 uninstall pypodo
pip uninstall pypodo
pip3 uninstall pypodo --break-system-packages
pip uninstall pypodo --break-system-packages
```

# Installation

```
pipx install pypodo
```

# Upgrade

```
pipx upgrade pypodo
pipx reinstall pypodo #to force update dependencies
```

# Uninstall

```
pipx uninstall pypodo
```


# Configuration [optional]

You can customize the application with the ``config`` file. Create it if it does not exist and copy paste this content. The autosort option runs a pypodo sort after pypodo del. The location of the config file can be obtained with ``pypodo --V``

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
#todofile = ~/.config/pypodo/todo
#todobackupfolder = ~/.config/pypodo/backup


[FONCTIONAL]
####int values
#periodalert = 0
#periodwarning = 7
####tags with '#' and with a coma separation
#alerttags = #urgent
####True to autosort todolist
#autosort = False
####True to auto condensate output
#condensate = False
####True to nocolor
#nocolor = False

```
# Use with newsboat [optional]

If you use [newsboat](https://github.com/newsboat/newsboat), you can modify the configuration of the rss reader to save url of your favorites articles with 'o' press.

```
browser "pypodo add '%u #rss'"
```

# File sharing [optional]

You can use the configuration file to change the path of your todofile. If you used a "cloud folder" as cozy drive, you can share your pypodo app between two or more computeurs!

