# pypodo

pypodo (\pipudu\\) is a pip package : a todolist program who works with a .todo file at the root of the home directory in your terminal

## Install

```
pip3 install --user git+https://github.com/thib1984/pypodo.git#egg=pypodo
```

## Upgrade

```
pip3 install --user git+https://github.com/thib1984/pypodo.git#egg=pypodo --upgrade
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

``pypodo`` 

display help message

``pypodo help``

display help message

``pypodo add "to do work #name_of_tag"``

add the task 'to do work' with the tag 'name_of_tag'

``pypodo add "to do other_work #name_of_other_tag" "to do other_big_work #name_of_other_tag"``

add the other task 'to do other_work' with the tag 'name_of_other_tag' the another task 'to do other_big_work' with the tag 'name_of_tag'

``pypodo list`` 

print the todolist with an index for each task :

```
1 to do work #name_of_tag
2 to do other_work #name_of_other_tag
3 to do other_big_work #name_of_other_tag
```


`` pypodo list "name_of_tag"``

print the todolist filtered to the tag name_of_tag :

```
1 to do work #name_of_tag
```

``pypodo del 2`` 

delete the second task of the todolist

``pypodo list``


print the todolist with an index for each task : 

```
1 to do work #name_of_tag
3 to do other_big_work #name_of_other_tag
```


``pypodo clear``

reorder the todolist in consecutives index


``pypodo list``
print the todolist with an index for each task :

```
1 to do work #name_of_tag
2 to do other_big_work #name_of_other_tag
```

``pypodo tag new_tag 1``

add a tag to the first task

``pypodo list``

print the todolist with an index for each task

```
1 to do work #name_of_tag #new_tag
2 to do other_big_work #name_of_other_tag
```

``pypodo untag new_tag 1``

remove tag new_tag from the first task

``pypodo list``

print the todolist with an index for each task :

```
1 to do work
2 to do other_big_work #name_of_other_tag
```

``pypodo tag new_tag 1 2``

add a tag to the first and second task

``pypodo list``

print the todolist with an index for each task :

```
1 to do work #new_tag
2 to do other_big_work #name_of_other_tag #new_tag
```

``pypodo unatag new_tag 1 2``

remove a tag  new_tag to the first and second task

``pypodo list``

print the todolist with an index for each task :

```
1 to do work 
2 to do other_big_work #name_of_other_tag
```

``pypodo del 1 2``

remove the 2 task 


## Uninstall

```
pip3 uninstall pypodo
```
