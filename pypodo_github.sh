#!/bin/bash
green="\e[32m"
red="\e[31m"
yellow="\e[33m"
default="\e[39m"
file_log_pylint=./pylint.log
file_log_build_docker_test=./build_test.log
file_log_build_docker_prod=./build_prod.log
file_log_configuration=./configuration.log
file_log_test=./test.log
file_log_coverage=./coverage.log
file_log_mutation=./mutation.log
file_log_end_to_end=./end_to_end.log
file_log_install=./install.log
folder_log_coverage=./htmlcov

dockerci () {
    #configuration
    printinfo "configuration running..."
    export PYPODO_FILE=/tmp/.todo
    export PYPODO_BACKUP=/tmp/.todo_backup
    export PYPODO_CONF=/tmp/.todo.rc
    smoketest="docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_CONF},target=/root/.todo.rc --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup thibaultgarcon/pypodo_test"
    dockerpypodorun="docker run --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_CONF},target=/root/.todo.rc --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup -ti"
    rm $PYPODO_FILE
    rm -rf $PYPODO_BACKUP
    rm $PYPODO_CONF
    touch $PYPODO_FILE && touch $PYPODO_CONF && mkdir $PYPODO_BACKUP
    #build
    printinfo "docker build running..."
    docker build -t thibaultgarcon/pypodo_test . --no-cache
    if [[ $? = 0 ]]
    then
        printinfo "docker build ok"
    else
        printerror "docker build ko"
        return 1
    fi
    printinfo "end-to-end 1/4 running..."
    diff <(./end_to_end.sh "$smoketest") <(cat ci_cd/log.expected)
    if [[ $? = 0 ]]
    then
        printinfo "test end-to-end 1/4 ok"
    else
        printerror "test end-to-end 1/4 ko"
        return 1
    fi
    printinfo "test end-to-end 2/4 running..."
    $smoketest backup | grep "\[32minfo    : creating todolist backup - .todo[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]" > /dev/null
    if [[ $? = 0 ]]
    then
        printinfo "test end-to-end 2/4 ok"
    else
        printerror "test end-to-end 2/4 ko"
        return 1
    fi
    printinfo "test end-to-end 3/3 running..."
    diff ${PYPODO_FILE} ci_cd/.todo.expected >> $file_log_end_to_end
    if [[ $? = 0 ]]
    then
        printinfo "test end-to-end 3/4 ok"
    else
        printerror "test end-to-end 3/4 ko"
        return 1
    fi
    printinfo "test end-to-end 4/4 running..."
    diff ${PYPODO_BACKUP}/.todo* ci_cd/.todo.expected >> $file_log_end_to_end
    if [[ $? = 0 ]]
    then
        printinfo "test end-to-end 4/4 ok"
    else
        printerror "test end-to-end 4/4 ko"
        return 1
    fi
}



printinfo () {
    echo -e $green"info    : "$1$default
}

printerror () {
    echo -e $red"error   : "$1$default
}

printwarning () {
    echo -e $yellow"warning : "$1$default
}

dockerci
if [[ $? = 0 ]]
then
    printinfo "docker ci ok"
else
    printerror "CI_CD FULL KO"
    exit 1
fi

