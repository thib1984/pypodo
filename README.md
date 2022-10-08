:warning: In the case of an update from 4.x version, with this version the location of the todo file, the config file and default backup folder change! Play ``pypodo --info`` to see the new location and move you actual config file.


# :ballot_box_with_check: pypodo

**pypodo** (\pipudu\\) is a pip package : a todolist tool which works in your terminal. It has a mecanism of indexes and tags.


# 💫 Demo

![image](./demo.gif))

# :book: How use **pypodo**

## :bird: Beginner

- ``pypodo`` print your actual todolist.

- ``pypodo --add/-a ITEM ...`` add items in the todolist

- ``pypodo --del/-d INDEX ...``* delete items by the indexes in your todolist

- ``pypodo --help/-h`` show the help message
## :airplane: Intermediate

- ``pypodo --tag TAG INDEX ...``* add a TAG at the items by the indexes

- ``pypodo --untag TAG INDEX ...``* remove a TAG at the items by the indexes

- ``pypodo --filter/-f TAG ...`` filter todolist with the tags given (cumulative filter)

- ``pypodo --exclude/-e TAG ...`` filter todolist with the tags given excluded (cumulative filter)

- ``pypodo --warning/-w TAG ...`` filter todolist with the alert or warning tags

## 🚀 Expert

- ``pypodo --day/-D -a ITEM`` add item with tag of the current day

- ``pypodo --week/-W -a ITEM`` add item with tag of the day + one week

- ``pypodo --month/-M -a ITEM`` add item with tag of the day + one month

- ``pypodo --order/-o`` reorder the todolist with consecutive indexes

- ``pypodo --backup/-b`` create a backup from the todolist in the backup folder, with timestamp suffix (todoYYYYMMddHHmmSS)

- ``pypodo --search/-s REGEX`` search regex given in the totolist

- ``pypodo --update/-u`` update pypodo with pip or pip3

- ``pypodo --info`` display informations about pypodo (version, location of files, ...)



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