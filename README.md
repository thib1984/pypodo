# pypodo

**pypodo** (\pipudu\\) is a pip package : a todolist tool which works with a .todo file positionned the root of the home directory

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

## Github

To work with Github
```
git clone https://github.com/thib1984/pypodo.git
cd pypodo
#work with git
pip3 install --user .
```

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

- ``pypodo sort`` :  reorder all tasks by index

- ``pypodo tag new_tag 1`` : add the tag '_new_tag_' to the first task

- ``pypodo untag new_tag 1`` : remove tag '_new_tag_' from the first task

- ``pypodo tag new_tag 1 2`` : add the tag '_new_tag_' to the first and second task

- ``pypodo unatag new_tag 1 2`` : remove the tag '_new_tag_' to the first and second task

- ``pypodo del 1 2`` : remove the 2 tasks 
