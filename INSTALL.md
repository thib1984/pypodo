# Install/Upgrade/Uninstall

## Python library

:warning: Not compatible with python2 who is deprecated! Use python3

```
pip3 install --user git+https://github.com/thib1984/pypodo.git#egg=pypodo #Installation
pip3 install --user git+https://github.com/thib1984/pypodo.git#egg=pypodo --upgrade #Upgrade
pip3 uninstall pypodo #Uninstall
```

## Docker usage [optionnal]

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


To remove docker app, just : `docker rmi pypodo`

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

## Alias [optionnal]

You can use alias as

```
#uncomment if you use docker app only
#alias pypodo="export PYPODO_FILE=<path of your pypodo file> && touch $PYPODO_FILE && export PYPODO_BACKUP=<path of your pypodo backup folder> && mkdir -p $PYPODO_BACKUP  && docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup pypodo"
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
## Use with newsboat [optional]

If you use [newsboat](https://github.com/newsboat/newsboat), you can modify the configuration of the rss reader to save url of your favorites articles with 'o' press.

```
browser "pypodo add '%u #rss'"
```

## File sharing [optional]

You can use the .todo.rc configuration file to change the path of your todofile. If you used a "cloud folder" as cozy drive, you can share your pypodo app between two or more computeurs!

## Crypt/Decrypt [optional]

In case of sharing, you can improve security, and activate encryption of your .todo file. For that, juste add a SYSTEM.key in your .todo.rc file. If your todo file is empty or non-existent, no additionnal config is needed. If you have a non-empty todo file, run ``pypodo crypt`` and replace the content of todo file with the content of ~/.todo.crypt file. ``cp ~/.todo.crypt ~/.todo`` for example.
