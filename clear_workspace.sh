#!/bin/bash
green="\e[32m"
red="\e[31m"
yellow="\e[33m"
default="\e[39m"

printinfo () {
    echo -e "$green""info    : ""$1$default"
}

printerror () {
    echo -e "$red""error   : ""$1$default"
}

printwarning () {
    echo -e "$yellow""warning : ""$1$default"
}


printinfo "clear is running..."
export PYPODO_FILE=/tmp/.todo
export PYPODO_BACKUP=/tmp/.todo_backup
export PYPODO_CONF=/tmp/.todo.rc
export PYPODO_FILE_CRYPT=/tmp/.todo.crypt
export PYPODO_FILE_DECRYPT=/tmp/.todo.decrypt
rm ./*.log 2> /dev/null
rm ci_cd/cache/*
docker rm pypodo_mutation
docker rm pypodo_coverage
docker rm pypodo_coverage_html
docker rmi thibaultgarcon/pypodo_coverage
docker rmi thibaultgarcon/pypodo_test
docker rmi pypodo_coverage_html
rm $PYPODO_FILE
rm $PYPODO_FILE_CRYPT
rm $PYPODO_FILE_DECRYPT
rm $PYPODO_CONF
rm -rf $PYPODO_BACKUP


printinfo "clear is finished"



