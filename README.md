# pypodo

**pypodo** (\pipudu\\) is a pip package (or docker image if you want, see below!) : a todolist tool which works with a .todo file positionned the root of the home directory

## Tanks to contributors

- https://github.com/bbougon
- https://github.com/isaacvv
- https://github.com/jeanphibaconnais

## Compatibility

:warning: Not compatible with python2 who is deprecated! Use python3

## Install/Upgrade/Uninstall

```
pip3 install --user git+https://github.com/thib1984/pypodo.git#egg=pypodo #Installation
pip3 install --user git+https://github.com/thib1984/pypodo.git#egg=pypodo --upgrade #Upgrade
pip3 uninstall pypodo #Uninstall
```

## Utilisation

Common commands are **list**/**add**/**del**/**tag**/**untag**

Other commands are **help**/**backup**/**sort**/**find**

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

## Screenshots

The indexes are in blue, the tasks in green, and the tags in yellow or red.

![image](https://user-images.githubusercontent.com/45128847/95683314-c75dd400-0bea-11eb-900c-bf1aafc09999.png)

## Docker usage :computer:

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

To remove docker app, just : ``docker rmi pypodo``


## Alias :computer:

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

to improve your velocity!


## Github :construction_worker:

To work with Github
```
git clone https://github.com/thib1984/pypodo.git #or your fork repo ;)
cd pypodo
#work with git
git add .
git commit -am "my commit"
git push
```

## Test :construction_worker:

```
#in the root of the project
python3 -m unittest -v pypodo/__pypodo__test.py #to execute unit tests
coverage run && coverage html #to generate html : report in htmlcov folder
mutatest #to test mutations #to generate mutations : report mutation.log
```
## Local CI/CD :construction_worker:

```
./pypodo_ci_cd.sh pip ci #to launch unit test, coverage and mutation
./pypodo_ci_cd.sh pip ci fast #to launch unit test and coverage
./pypodo_ci_cd.sh pip cd #to launch unit test, coverage, and mutation + build pip
./pypodo_ci_cd.sh pip cd fast #to launch unit test and coverage + build pip
./pypodo_ci_cd.sh docker ci #to launch unit test, coverage, mutation and end to end test with docker
./pypodo_ci_cd.sh docker ci fast #to launch unit test, coverage and end to end test with docker
./pypodo_ci_cd.sh docker cd #to launch unit test, coverage, mutation and end to end test with docker + build image pypodo
./pypodo_ci_cd.sh docker cd fast #to launch unit test, coverage and end to end test with docker + build image pypodo
./pypodo_ci_cd.sh full #to launch unit test, coverage, mutation and end to end test with docker + build pip + build image pypodo
./pypodo_ci_cd.sh full fast #to launch unit test, coverage and end to end test with docker + build pip + build image pypodo

```
