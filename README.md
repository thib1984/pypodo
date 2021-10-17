
# 🐍 pypodo

**pypodo** (\pipudu\\) is a pip package (or docker image if you want, see below !) : a todolist tool which works with a .todo file positionned the root of the home directory.


# 💫 Demo

![image](https://user-images.githubusercontent.com/45128847/137579798-1d0fb4b9-6cd1-473d-805c-43f657673694.gif))

# 🚀 How use **pypodo**

Common commands are **list**/**add**/**del**/**tag**/**untag**. Others commands are **help**/**backup**/**sort**/**find**.

- `pypodo add "to do work #name_of_tag"` : add the task '_to do work_' with the tag '_name_of_tag_'

- `pypodo add "to do other_work #name_of_other_tag" "to do other_big_work #name_of_other_tag"` : add multi-task

- ``pypodo list`` : display the todolist with the index of each task

```
1 to do work #name_of_tag
2 to do other_work #name_of_other_tag
3 to do other_big_work #name_of_other_tag
```

- ` pypodo list "name_of_tag"`

print the todolist filtered to the tag '_name_of_tag_' :

```
1 to do work #name_of_tag
```

- ` pypodo list "name_of_tag" "other_tag"` : print the todolist filtered to tasks with the 2 tags together

- `pypodo del 2` : delete the second task of the todolist

- `pypodo del 1 2` : remove the 2 tasks

- `pypodo tag new_tag 1` : add the tag '_new_tag_' to the first task

- `pypodo tag new_tag 1 2` : add the tag '_new_tag_' to the first and second task

- `pypodo tag` : display all tags of the todolist

- `pypodo untag new_tag 1` : remove tag '_new_tag_' from the first task

- `pypodo untag new_tag 1 2` : remove the tag '_new_tag_' to the first and second task

- `pypodo untag` : display all tasks without tags

- `pypodo sort` : reorder all tasks by index

- `pypodo backup` : backup the actual .todo in a backup folder with a name suffixed by a timestamp

- `pypodo find "t.*he"` : filter the todolist on the parameter (regex format)

- `pypodo crypt admin` : crypt the todolist in the ~/.todo.crypt file with key "admin"

- `pypodo crypt` : crypt the todolist in the ~/.todo.crypt file with key in the config file SYSTEM.key

- `pypodo decrypt admin` : decrypt the crypted todolist in the ~/.todo.decrypt file with key "admin"

- `pypodo decrypt` : decrypt the crypted todolist in the ~/.todo.decrypt file with key in the config file SYSTEM.key

- `pypodo help` : display help message

- `pypodo` : display help message

# ⚙️ Install

See [this page](INSTALL.md) to improve your velocity !

# :construction_worker: Contribution

## For contributors

Go to [CONTRIBUTING.md](CONTRIBUTING.md).

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Tanks to contributors

- https://github.com/bbougon
- https://github.com/isaacvv
- https://github.com/jeanphibaconnais
