
# 🐍 pypodo

**pypodo** (\pipudu\\) is a pip package (or docker image if you want, see below !) : a todolist tool which works with a .todo file positionned the root of the home directory.


# 💫 Demo

![image](./demo.gif))

# 🚀 How use **pypodo**

- ``pypodo `` print your actual todolist.

- ``pypodo --add/-a ITEM ... `` add items in the todolist

- ``pypodo --del/-d INDEX ... `` delete items by the indexes in your todolist

- ``pypodo --tag/-t TAG INDEX ... `` add a TAG at the items by the indexes

- ``pypodo --untag/-u TAG INDEX ... `` remove a TAG at the items by the indexes

- ``pypodo --filter/-f TAG ... `` filter todolist with the tags given

- ``pypodo --order/-o `` reorder the todolist with consecutive indexes

- ``pypodo --backup/-b `` create a backup from the todolist in ~/.todoabckup folder

- ``pypodo --search/-s REGEX `` search regex given in the totolist

- ``pypodo --update/-U `` update pypodo with pip or pip3

- ``pypodo --version/-V `` display the version of pypodo

- ``pypodo --help/-h `` show the help message

You can also add other options :

- `` --nocolor/-n `` disable colour in sysout

- `` --verbose/-v `` verbose mode

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
