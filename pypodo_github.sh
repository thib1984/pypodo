#!/bin/bash
green="\e[32m"
red="\e[31m"
yellow="\e[33m"
default="\e[39m"

dockerci () {
    #configuration
    printinfo "configuration running..."
    export PYPODO_FILE=/tmp/.todo
    export PYPODO_BACKUP=/tmp/.todo_backup
    export PYPODO_CONF=/tmp/.todo.rc
    export PYPODO_FILE_DECRYPT=/tmp/.todo.decrypt
    export PYPODO_FILE_CRYPT=/tmp/.todo.crypt
    smoketest="docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_CONF},target=/root/.todo.rc --mount type=bind,source=${PYPODO_FILE_CRYPT},target=/root/.todo.crypt --mount type=bind,source=${PYPODO_FILE_DECRYPT},target=/root/.todo.decrypt --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup thibaultgarcon/pypodo_test"
    rm $PYPODO_FILE
    rm -rf $PYPODO_BACKUP
    rm $PYPODO_CONF
    rm $PYPODO_FILE_CRYPT
    rm $PYPODO_FILE_DECRYPT
    touch $PYPODO_FILE && touch $PYPODO_CONF && touch $PYPODO_FILE_CRYPT && touch $PYPODO_FILE_DECRYPT && mkdir $PYPODO_BACKUP
    #build
    printinfo "docker build running..."
    if docker build -t thibaultgarcon/pypodo_test . --no-cache;
    then
        printinfo "docker build ok"
    else
        printerror "docker build ko"
        return 1
    fi
    printinfo "test end-to-end 1/6 running... compare log"
    if diff <(./ci_cd/end_to_end.sh "$smoketest") <(cat ci_cd/log.expected);
    then
        printinfo "test end-to-end 1/6 ok"
    else
        printerror "test end-to-end 1/6 ko"
        return 1
    fi
    printinfo "test end-to-end 2/6 running... compare backup log"
    if  $smoketest backup | grep "\[32minfo    : creating todolist backup - .todo[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]" > /dev/null;
    then
        printinfo "test end-to-end 2/6 ok"
    else
        printerror "test end-to-end 2/6 ko"
        return 1
    fi
    printinfo "test end-to-end 3/4 running... compare todofile"
    if diff ${PYPODO_FILE} ci_cd/.todo.expected;
    then
        printinfo "test end-to-end 3/6 ok"
    else
        printerror "test end-to-end 3/6 ko"
        return 1
    fi
    printinfo "test end-to-end 4/6 running... compare todobackupfile"
    if diff ${PYPODO_BACKUP}/.todo* ci_cd/.todo.expected;
    then
        printinfo "test end-to-end 4/6 ok"
    else
        printerror "test end-to-end 4/6 ko"
        return 1
    fi
    printinfo "test end-to-end 5/6 running... compare log with special conf"
    rm "$PYPODO_FILE"
    touch "$PYPODO_FILE"
    cp ./ci_cd/.todo.rc $PYPODO_CONF
    if diff <(./ci_cd/end_to_end.sh "$smoketest") <(cat ci_cd/log.with.conf.expected);
    then
        printinfo "test end-to-end 5/6 ok"
    else
        printerror "test end-to-end 5/6 ko"
        return 1
    fi
    printinfo "test end-to-end 6/6 running... compare log with special conf"
    if  diff ${PYPODO_FILE_DECRYPT} ci_cd/.todo.expected.decrypt;
    then
        printinfo "test end-to-end 6/6 ok"
    else
        printerror "test end-to-end 6/6 ko"
        return 1
    fi
    
}



printinfo () {
    echo -e "$green""info    : ""$1$default"
}

printerror () {
    echo -e "$red""error   : ""$1$default"
}

printwarning () {
    echo -e "$yellow""warning : ""$1$default"
}

if dockerci;
then
    printinfo "docker ci ok"
else
    printerror "CI_CD FULL KO"
    exit 1
fi

