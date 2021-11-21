
# :ballot_box_with_check: pypodo

**pypodo** (\pipudu\\) is a pip package : a todolist tool which works with a .todo file positionned the root of the home directory.


# 💫 Demo

![image](./demo.gif))

# :book: How use **pypodo**

## :bird: Beginner

- ``pypodo`` print your actual todolist.

- ``pypodo --add/-a ITEM ...`` add items in the todolist

- ``pypodo --del/-d INDEX ...``* delete items by the indexes in your todolist

- ``pypodo --help/-h`` show the help message
## :airplane: Intermediate

- ``pypodo --tag/-t TAG INDEX ...``* add a TAG at the items by the indexes

- ``pypodo --untag/-u TAG INDEX ...``* remove a TAG at the items by the indexes

- ``pypodo --filter/-f TAG ...`` filter todolist with the tags given (cumulative filter)

## 🚀 Expert

- ``pypodo --order/-o`` reorder the todolist with consecutive indexes

- ``pypodo --backup/-b`` create a backup from the todolist in ~/.todo_backup folder, with timestamp suffix (.todoYYYYMMddHHmmSS)

- ``pypodo --search/-s REGEX`` search regex given in the totolist

- ``pypodo --update/-U`` update pypodo with pip or pip3

- ``pypodo --version/-V`` display the version of pypodo



You can also add other options :

- `` --nocolor/-n`` disable colour in sysout (overwrite the config file)

- `` --verbose/-v`` verbose mode  (overwrite the config file)

- `` --condensate/-c`` condensate mode

*for ``INDEX ...``, we can use short expression for consecutives index : for example, you can replace 2 3 4 by 2-4 

# ⚙️ Install

See [this page](INSTALL.md) to improve your velocity !

# :construction_worker: Contribution


Go to [CONTRIBUTING.md](CONTRIBUTING.md).

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

Tanks to contributors :

- https://github.com/bbougon
- https://github.com/isaacvv
- https://github.com/jeanphibaconnais

# :package: Changelog


See [this page](CHANGELOG.md)
# :pencil: License

MIT License

Copyright (c) 2021 [thib1984](https://github.com/thib1984)

See [this page](LICENSE.txt) for details