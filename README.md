# pytodo

pytodo is a todolist programm who works with a .todo file at the root of the home directory

## Install

```
git clone https://github.com/thib1984/pytodo.git
cd pytodo
pip3 install --user .
```
or directly
```
pip3 install --user git+https://github.com/thib1984/pytodo.git#egg=pytodo
```

## Utilisation

```
pytodo-add "to do work #name_of_tag" #add the task 'to do work' with the tag 'name_of_tag'
pytodo-add "to do other_work #name_of_other_tag" #add the other task 'to do other_work' with the tag 'name_of_other_tag'
pytodo-add "to do other_big_work #name_of_other_tag" #add the other task 'to do other_big_work' with the tag 'name_of_tag'
pytodo-list #print the todolist with an index for each task
pytodo-list "name_of_tag" #print the todolist filtered to the tag name_of_tag
pytodo-del 2 #delete the second task of the todolist
pytodo-clear #reorder the todolist in consecutives index
```

## Uninstall

```
pip3 uninstall pytodo
```
