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

```
git clone https://github.com/thib1984/pypodo.git
cd pypodo
docker build -t pypodo .
```

to construct the docker image
And your pypodo app is available 🤘 !

and

```
export PYPODO_FILE=<path of your pypodo file>
touch $PYPODO_FILE
export PYPODO_BACKUP=<path of your pypodo backup folder>
mkdir -p $PYPODO_BACKUP
docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup pypodo
```

to use it

If you don't want to write all this command at each time, you can create an alias :

```
alias pypodo="export PYPODO_FILE=<path of your pypodo file> && touch $PYPODO_FILE && export PYPODO_BACKUP=<path of your pypodo backup folder> && mkdir -p $PYPODO_BACKUP  && docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup pypodo"
```

or for a full time usage, change your `.bash_profile` file, and if you want use aliases in alias section after!

To remove docker app, just : `docker rmi pypodo`

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
