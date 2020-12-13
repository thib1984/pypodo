# pypodo

**pypodo** (\pipudu\\) is a pip package (or docker image if you want, see below!). It is a todolist tool which works with a .todo file at the root of the home directory. It has a mecanism of indexes and tags.

## Install/Upgrade/Uninstall

:warning: Not compatible with python2 (deprecated), Use python3.

```
pip3 install pypodo #Installation, use pip if pip3 does not exist
pip3 install pypodo --upgrade #Upgrade, use pip if pip3 does not exist
pip3 uninstall pypodo #Uninstall, use pip if pip3 does not exist
```

After the install, restart the system or play 'source ~/.profile' to access directly pypodo commands. 

[https://pypi.org/project/pypodo/](https://pypi.org/project/pypodo/)

## Use

Usual commands are **list**/**add**/**del**/**tag**/**untag**

Other commands are **help**/**backup**/**sort**/**find**/**crypt**/**decrypt**

- ``pypodo add "to do work #name_of_tag"`` : add one task '_to do work_' with the tag '_name_of_tag_'

- ``pypodo add "to do other_work #name_of_other_tag" "to do other_big_work #name_of_other_tag"`` : add one task '_to do other_work_' with the tag '_name_of_other_tag_' and another task '_to do other_big_work_' with the tag 'name_of_other_tag'

- ``pypodo list`` : display the todolist with the index of each task

```
1 to do work #name_of_tag
2 to do other_work #name_of_other_tag
3 to do other_big_work #name_of_other_tag
```

The default color of the tags is green. When a task is tagged "#urgent" it will be colored in red. When the task has a date pattern like YYYYmmdd with a gap to current date less than seven days, it will be colored in yellow. If the date is greater than the current date, in red . See the Configuration to change the colors.

- `` pypodo list "name_of_tag"`` : display the todolist filtered on the tasks tagged with '_name_of_tag_'

```
1 to do work #name_of_tag
```

- `` pypodo list "name_of_tag" "other_tag"`` : display the todolist filtered on the tasks tagged with both tags

- ``pypodo del 2``  : delete the task with index=2 of the todolist

- ``pypodo del 1 2`` : remove the 2 tasks (index=1 and index=2)

- ``pypodo del 2-4`` : remove the 3 tasks (from index=2 to index=4)

- ``pypodo tag new_tag 1`` : add the tag '_new_tag_' to the task with index=1

- ``pypodo tag new_tag 1 2`` : add the tag '_new_tag_' to both tasks index=1 and index=2

- ``pypodo tag new_tag 2-4`` : add the tag '_new_tag_' to the 3 tasks (from index=2 to index=4)

- ``pypodo tag`` : display all tags of the todolist

- ``pypodo untag new_tag 1`` : remove tag '_new_tag_' from the task with index=1

- ``pypodo untag new_tag 1 2`` : remove the tag '_new_tag_' from both tasks index=1 and index=2

- ``pypodo tag new_tag 2-4`` : remove the tag '_new_tag_' from the 3 tasks (from index=2 to index=4)

- ``pypodo untag`` : display all tasks without tags

- ``pypodo sort`` :  reorder all tasks by index

- ``pypodo backup`` : backup the actual .todo in a backup folder with a filename suffixed by a timestamp

- ``pypodo find "t.*he"`` : filter the todolist on the parameter (regex format accepted)

- ``pypodo crypt admin`` : crypt the todolist in the ~/.todo.crypt file with key "admin"

- ``pypodo crypt`` : crypt the todolist in the ~/.todo.crypt file with key in the config file SYSTEM.key

- ``pypodo decrypt admin`` : decrypt the crypted todolist in the ~/.todo.decrypt file with key "admin"

- ``pypodo decrypt`` : decrypt the crypted todolist in the ~/.todo.decrypt file with key in the config file SYSTEM.key

- ``pypodo help`` : display help message

- ``pypodo`` : display help message


## Screenshots

Example of commands

![image](https://user-images.githubusercontent.com/45128847/95683314-c75dd400-0bea-11eb-900c-bf1aafc09999.png)

Color of tags at the 19/10/2020 : red alert for one task, yellow warning for the second, default for the third.

![image](https://user-images.githubusercontent.com/45128847/96498585-88fc9080-124c-11eb-9050-4adacb7204a1.png)

## Configuration [optional]

You can customize the application with the ``~/.todo.rc`` file. Create it if it does not exist and copy paste this content. The autosort option runs a pypodo sort after pypodo del.

```
#grey,red,green,yellow,blue,magenta,cyan,white only ;)
[COLOR]
alert = red
warning = yellow
info = green
index = blue
task = green
tag = cyan
debug = grey

[SYSTEM]
#debug,info,warning,error
messagelevel = info
#format double % character, use for warning and alert on dates
#formatdate = %%Y%%m%%d
#not modify if you use docker!
#todofile = /tmp/.todo
#todobackupfolder = /tmp/.todo_backup/
#use if your todofile is exposed
#key=admin

[FONCTIONAL]
#int values
periodalert = 0
periodwarning = 7
#tags with '#' and with a coma separation
alerttags = #urgent
#or True
autosort = False
```

## Docker usage [optional]

If you want, you can use **pypodo** as a docker image.

Copy file [docker-pypodo.sh](https://github.com/thib1984/pypodo/blob/master/docker-pypodo.sh) on your PC.
Give execution permission with ``chmod u+x ./docker-pypodo.sh``
Correct the two variables (optional) :

```
PYPODO_FILE=~/.todo
PYPODO_FILE_CRYPT=~/.todo.crypt
PYPODO_FILE_DECRYPT=~/.todo.decrypt
PYPODO_BACKUP=~/.todo_backup
PYPODO_CONFIG=~/.todo.rc
```

and test you app! :

```
./docker-pypodo.sh help
```

Replace ``pypodo`` with ``./docker-pypodo.sh`` or use an alias (see below)

You can see [the repo docker](https://hub.docker.com/r/thibaultgarcon/pypodo)

## Alias [optional]

You can use alias as

```
#uncomment if you use docker app only with the correct directory
#alias pypodo=~/docker-pypodo.sh
#for all apps
alias tl='pypodo list'
alias ta='pypodo add'
alias tt='pypodo tag'
alias td='pypodo del'
alias ts='pypodo sort'
alias tu='pypodo untag'
alias tb='pypodo backup'
alias tf='pypodo find'
```

to improve your efficiency!

## Use with newsboat [optional]

If you use [newsboat](https://github.com/newsboat/newsboat), you can modify the configuration of the rss reader to save url of your favorites articles with 'o' press.

```
browser "pypodo add '%u #rss'"
```


## File sharing [optional]

You can use the .todo.rc configuration file to change the path of your todofile. If you used a "cloud folder" as cozy drive, you can share your pypodo app between two or more computeurs!

## Crypt/Decrypt [optional]

In case of sharing, you can improve security, and activate encryption of your .todo file. For that, juste add a SYSTEM.key in your .todo.rc file. If your todo file is empty or non-existent, no additionnal config is needed. If you have a non-empty todo file, run ``pypodo crypt`` and replace the content of todo file with the content of ~/.todo.crypt file. ``cp ~/.todo.crypt ~/.todo`` for example.

## Changelog

### 3.0.3 -WIP-

- Add new parameter formatlist for index : "1-3" for example

### 3.0.2

- Optimize docker image size
- Correction if incorrect path todofile
- Correction if permission errors
- For dev only : Clean test classe
- For dev only : Add clear_workspace script
- For dev only : Use of  ubuntu 20.04 for Github Actions

### 3.0.1

- Improve debug messages
- Correction of minor bugs in docker test
- the '#' character can be place in the task if it not preceded of an empty space

### 3.0.0

- Debug level
- Crypt/Decrypt todofile

### 2.3.2

- Code cleanup
- Increased test coverage
- Adding formatdate in configuration file
- Documentation corrections

## For contributors :construction_worker:

[Go to CONTRIBUTING.md](https://github.com/thib1984/pypodo/blob/master/CONTRIBUTING.md)

## Thanks to contributors
- https://github.com/bbougon
- https://github.com/isaacvv
- https://github.com/jeanphibaconnais
