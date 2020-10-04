# pytodolist

pytodolist is a pip package : a todolist program who works with a .todo file at the root of the home directory in your terminal

## Install

```
pip3 install --user git+https://github.com/thib1984/pytodolist.git#egg=pytodolist
```

## Upgrade

```
pip3 install --user git+https://github.com/thib1984/pytodolist.git#egg=pytodolist --upgrade
```

## Github

To work with Github
```
git clone https://github.com/thib1984/pytodolist.git
cd pytodolist
#work with git
pip3 install --user .
```

## Utilisation

``pytodo`` 

display help message

``pytodo help``

display help message

``pytodo add "to do work #name_of_tag"``

add the task 'to do work' with the tag 'name_of_tag'

``pytodo add "to do other_work #name_of_other_tag"``

add the other task 'to do other_work' with the tag 'name_of_other_tag'

``pytodo add "to do other_big_work #name_of_other_tag"``

add the other task 'to do other_big_work' with the tag 'name_of_tag'


``pytodo list`` 

print the todolist with an index for each task :

```
1 to do work #name_of_tag
2 to do other_work #name_of_other_tag
3 to do other_big_work #name_of_other_tag
```


`` pytodo list "name_of_tag"``

print the todolist filtered to the tag name_of_tag :

```
1 to do work #name_of_tag
```

``pytodo del 2`` 

delete the second task of the todolist

``pytodo list``


print the todolist with an index for each task : 

```
1 to do work #name_of_tag
3 to do other_big_work #name_of_other_tag
```


``pytodo clear``

reorder the todolist in consecutives index


``pytodo list``
print the todolist with an index for each task :

```
1 to do work #name_of_tag
2 to do other_big_work #name_of_other_tag
```

``pytodo tag 1 new_tag``

add a tag to the first task

``pytodo list``

print the todolist with an index for each task

```
1 to do work #name_of_tag #new_tag
2 to do other_big_work #name_of_other_tag
```

``pytodo untag 1``

remove tags from the first task

``pytodo list``

print the todolist with an index for each task :

```
1 to do work
2 to do other_big_work #name_of_other_tag
```

## Uninstall

```
pip3 uninstall pytodolist
```
