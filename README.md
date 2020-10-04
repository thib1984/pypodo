# pytodo

pytodo is a todolist program who works with a .todo file at the root of the home directory

## Install

```
git clone https://github.com/thib1984/pytodolist.git
cd pytodolist
pip3 install --user .
```
or 
```
pip3 install --user git+https://github.com/thib1984/pytodolist.git#egg=pytodolist
```

## Utilisation

```
pytodo #display help
pytodo help #display help
pytodo add "to do work #name_of_tag" #add the task 'to do work' with the tag 'name_of_tag'
pytodo add "to do other_work #name_of_other_tag" #add the other task 'to do other_work' with the tag 'name_of_other_tag'
pytodo add "to do other_big_work #name_of_other_tag" #add the other task 'to do other_big_work' with the tag 'name_of_tag'
pytodo list #print the todolist with an index for each task
>1 to do work #name_of_tag
>2 to do other_work #name_of_other_tag
>3 to do other_big_work #name_of_other_tag
pytodo list "name_of_tag" #print the todolist filtered to the tag name_of_tag
>1 to do work #name_of_tag
pytodo del 2 #delete the second task of the todolist
pytodo list #print the todolist with an index for each task
>1 to do work #name_of_tag
>3 to do other_big_work #name_of_other_tag
pytodo clear #reorder the todolist in consecutives index
pytodo list #print the todolist with an index for each task
>1 to do work #name_of_tag
>2 to do other_big_work #name_of_other_tag
pytodo tag 1 new_tag #add a tag to the first task
pytodo list #print the todolist with an index for each task
>1 to do work #name_of_tag #new_tag
>2 to do other_big_work #name_of_other_tag
pytodo untag 1 #remove tags from the first task
pytodo list #print the todolist with an index for each task
>1 to do work
>2 to do other_big_work #name_of_other_tag
```

## Uninstall

```
pip3 uninstall pytodolist
```
