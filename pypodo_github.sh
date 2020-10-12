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
    #partie configuration
    printinfo "configuration running..."
    export PYPODO_FILE=/tmp/.todo
    export PYPODO_BACKUP=/tmp/.todo_backup
    dockerpypodorun="docker run --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup -i"
    smoketest="docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup pypodo_test"
    touch $PYPODO_FILE && mkdir $PYPODO_BACKUP 
    #partie build
    printinfo "docker build running..."
    docker build -t pypodo_test . --no-cache
    if [[ $? = 0 ]]
    then
        printinfo "docker build ok"
    else
        printerror "docker build ko"
        return 1
    fi
    #partie unittest
    $dockerpypodorun --rm --entrypoint="python" pypodo_test -m unittest -v pypodo/__pypodo__test.py
    if [[ $? = 0 ]]
    then
        printinfo "unittest ok"
    else
        printerror "unittest ko"
        return 1
    fi
    #partie end-to-end
    printinfo "end-to-end 1/4 running..."
    (echo pypodo list
        $smoketest list
        echo pypodo add "tache1"
        $smoketest add "tache1"
        echo pypodo add "tache2 #montag"
        $smoketest add "tache2 #montag"
        echo pypodo add "tache3 #urgent"
        $smoketest add "tache3 #urgent"
        echo pypodo list
        $smoketest list
        echo pypodo del 2
        $smoketest del 2
        echo pypodo tag montag2 3
        $smoketest tag montag2 3
        echo pypodo ag urgente 3
        $smoketest tag urgente 3
        echo pypodo sort
        $smoketest sort
        $smoketest add "mon autre tache #tag #retag"
        echo pypodo list tag retag
        $smoketest list tag retag
        echo pypodo untag retag 3
        $smoketest untag retag 3
        echo pypodo tag newtag 3 3 2
        $smoketest tag newtag 3 3 2
        echo pypodo list
        $smoketest list
        echo pypodo tag
        $smoketest tag
        echo pypodo untag
        $smoketest untag
        echo pypodo find "t.*che"
    $smoketest find "t.*che")
    $smoketest backup
    diff ci_cd/cache/log ci_cd/log.expected >> $file_log_end_to_end
    if [[ $? = 0 ]]
    then
        printinfo "test end-to-end 1/4 ok, see output in $file_log_end_to_end"
    else
        printerror "test end-to-end 1/4 ko, see output in $file_log_end_to_end"
        return 1
    fi
    printinfo "test end-to-end 2/4 running..."
    grep "\[32minfo : creating todolist backup - .todo[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]" ci_cd/cache/log_backup >> $file_log_end_to_end
    if [[ $? = 0 ]]
    then
        printinfo "test end-to-end 2/4 ok, see output in $file_log_end_to_end"
    else
        printerror "test end-to-end 2/4 ko, see output in $file_log_end_to_end"
        return 1
    fi
    printinfo "test end-to-end 3/3 running..."
    diff ${PYPODO_FILE} ci_cd/.todo.expected >> $file_log_end_to_end
    if [[ $? = 0 ]]
    then
        printinfo "test end-to-end 3/4 ok, see output in $file_log_end_to_end"
    else
        printerror "test end-to-end 3/4 ko, see output in $file_log_end_to_end"
        return 1
    fi
    printinfo "test end-to-end 4/4 running..."
    diff ${PYPODO_BACKUP}/.todo* ci_cd/.todo.expected >> $file_log_end_to_end
    if [[ $? = 0 ]]
    then
        printinfo "test end-to-end 4/4 ok, see output in $file_log_end_to_end"
    else
        printerror "test end-to-end 4/4 ko, see output in $file_log_end_to_end"
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

