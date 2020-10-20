# pypodo

**pypodo** (\pipudu\\) is a pip package (or docker image if you want, see below!) : a todolist tool which works with a .todo file positionned the root of the home directory with a mecanism of index and tags.

## Install/Upgrade/Uninstall

:warning: Not compatible with python2 who is deprecated! Use python3

```
pip3 install --user pypodo #Installation
pip3 install --user pypodo --upgrade #Upgrade
pip3 uninstall pypodo #Uninstall
```

[https://pypi.org/project/pypodo/](https://pypi.org/project/pypodo/)

## Utilisation

Common commands are **list**/**add**/**del**/**tag**/**untag**

Other commands are **help**/**backup**/**sort**/**find**

- ``pypodo add "to do work #name_of_tag"`` : add the task '_to do work_' with the tag '_name_of_tag_'

- ``pypodo add "to do other_work #name_of_other_tag" "to do other_big_work #name_of_other_tag"``

add the other task '_to do other_work_' with the tag '_name_of_other_tag_' the another task '_to do other_big_work_' with the tag '_name_of_tag_'

- ``pypodo list`` 

print the todolist with an index for each task :

```
1 to do work #name_of_tag
2 to do other_work #name_of_other_tag
3 to do other_big_work #name_of_other_tag
```
The tags are colored by default in green. If they are "#urgent" they are colored in red. If they have a date format YYYYmmdd and a gap to actual date less than seven days they are colored in yellow or red if greater than the actual date.

- `` pypodo list "name_of_tag"``

print the todolist filtered to the tag '_name_of_tag_' :

```
1 to do work #name_of_tag
```

- `` pypodo list "name_of_tag" "other_tag"`` : print the todolist filtered to tasks with the 2 tags together

- ``pypodo del 2``  : delete the second task of the todolist

- ``pypodo del 1 2`` : remove the 2 tasks 

- ``pypodo tag new_tag 1`` : add the tag '_new_tag_' to the first task

- ``pypodo tag new_tag 1 2`` : add the tag '_new_tag_' to the first and second task

- ``pypodo tag`` : display all tags of the todolist

- ``pypodo untag new_tag 1`` : remove tag '_new_tag_' from the first task

- ``pypodo untag new_tag 1 2`` : remove the tag '_new_tag_' to the first and second task

- ``pypodo untag`` : display all tasks without tags

- ``pypodo sort`` :  reorder all tasks by index

- ``pypodo backup`` : backup the actual .todo in a backup folder with a name suffixed by a timestamp

- ``pypodo find "t.*he"`` : filter the todolist on the parameter (regex format)

- ``pypodo help`` : display help message

- ``pypodo`` : display help message


## Screenshots

Example of commands

![image](https://user-images.githubusercontent.com/45128847/95683314-c75dd400-0bea-11eb-900c-bf1aafc09999.png)

Color of tags at the 19/10/2020 : red alert for one task, yellow warning for the second, nothing for the third.

![image](https://user-images.githubusercontent.com/45128847/96498585-88fc9080-124c-11eb-9050-4adacb7204a1.png)

## Configuration [optionnal]

You can customize the application with the ``~/.todo.rc`` file. Create it if it does not exist and copy paste these content. For now, you can modify the colors.

```
#grey,red,green,yellow,blue,magenta,cyan,white only ;)
[COLOR]
alert = red
warning = yellow
info = green
index = yellow
task = green
tag = cyan
```

## Docker usage [optionnal]

If you want, you can use **pypodo** as a docker image.

Copy file [docker-pypodo.sh](https://github.com/thib1984/pypodo/blob/master/docker-pypodo.sh) on your PC.
Give execution permission with ``chmod u+x ./docker-pypodo.sh``
Correct the two variables if you want :

```
PYPODO_FILE=~/.todo
PYPODO_BACKUP=~/.todo_backup
```

and test you app! :

```
./docker-pypodo.sh help
```

Replace ``pypodo`` with ``./docker-pypodo.sh`` or use an alias (see below)

You can see [the repo docker](https://hub.docker.com/r/thibaultgarcon/pypodo)

## Alias [optionnal]

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

to improve your velocity!

## For contributors :construction_worker:

[Go to CONTRIBUTING.md](https://github.com/thib1984/pypodo/blob/master/CONTRIBUTING.md)


## Tanks to contributors 
- https://github.com/bbougon
- https://github.com/isaacvv
- https://github.com/jeanphibaconnais
