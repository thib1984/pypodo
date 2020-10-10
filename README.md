# pypodo

**pypodo** (\pipudu\\) is a pip package : a todolist tool which works with a .todo file positionned the root of the home directory

## Tanks to contributors

- https://github.com/bbougon
- https://github.com/isaacvv
- https://github.com/jeanphibaconnais

## Compatibility

:warning: Not compatible with python2 who is deprecated! Use python3

## Install

```
pip3 install --user git+https://github.com/thib1984/pypodo.git#egg=pypodo
```

## Upgrade

```
pip3 install --user git+https://github.com/thib1984/pypodo.git#egg=pypodo --upgrade
```

## Uninstall

```
pip3 uninstall pypodo
```

## Docker usage

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

or for a full time usage, change your ```.bash_profile``` file, and if you want use aliases in alias section after!

## Utilisation

- ``pypodo`` : display help message

- ``pypodo help`` : display help message

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


- `` pypodo list "name_of_tag"``

print the todolist filtered to the tag '_name_of_tag_' :

```
1 to do work #name_of_tag
```

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


## Alias

You can use alias as

```
#if you use docker app only
alias pypodo="export PYPODO_FILE=<path of your pypodo file> && touch $PYPODO_FILE && export PYPODO_BACKUP=<path of your pypodo backup folder> && mkdir -p $PYPODO_BACKUP  && docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup pypodo"
#for all apps
alias tl='pypodo list'
alias ta='pypodo add'
alias tt='pypodo tag'
alias td='pypodo del'
alias ts='pypodo sort'
alias tu='pypodo untag'
alias tb='pypodo backup'
```

to improve your velocity!


## Github

To work with Github
```
git clone https://github.com/thib1984/pypodo.git #or your fork repo ;)
cd pypodo
#work with git
git add .
git commit -am "my commit"
git push
```

## Test

```
python3 -m unittest -v pypodo/__pypodo__test.py # to execute unit tests
coverage run && coverage html #to generate html report in htmlcov
mutatest #to test mutations
```
## Local CI/CD

```
./pytodo_ci_cd.sh pip #to launch unit test, coverage mutation, and build pip if ok 
./pytodo_ci_cd.sh docker #to create docker image_test, launch unit test, coverage mutation, and "end-to-end" test and build docker image app if ok 
./pytodo_ci_cd.sh full #to create docker image_test, launch unit test, coverage mutation, and "end-to-end" test and build docker image app  + pip if ok 
```