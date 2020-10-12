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
    (rm *.log
        rm ci_cd/cache/*
        touch $file_log_coverage $file_log_mutation $file_log_configuration $file_log_build_docker_test $file_log_test $file_log_pylint $file_log_build_docker_prod
        docker rm pypodo_mutation
        docker rm pypodo_coverage
        docker rm pypodo_coverage_html
        docker rmi pypodo_coverage
        docker rmi pypodo_test
    docker rmi pypodo_coverage_html) 1>> $file_log_configuration 2>> $file_log_configuration
    #for github?
    export COMPOSE_INTERACTIVE_NO_CLI=1
    export PYPODO_FILE=/tmp/.todo && touch $PYPODO_FILE && rm $PYPODO_FILE && touch $PYPODO_FILE 2>> $file_log_configuration
    export PYPODO_BACKUP=/tmp/.todo_backup && rm -rf $PYPODO_BACKUP && mkdir $PYPODO_BACKUP 2>> $file_log_configuration
    smoketest="docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup pypodo_test" 2>> $file_log_configuration
    dockerpypodorun="docker run --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup -i" 2>> $file_log_configuration
    printinfo "configuration ok, see output in $file_log_configuration"
    #partie build
    printinfo "docker build running..."
    docker build -t pypodo_test . --no-cache 1>>$file_log_build_docker_test 2>>$file_log_build_docker_test
    if [[ $? = 0 ]]
    then
        printinfo "docker build ok, see output in .$file_log_build_docker_test"
    else
        printerror "docker build ko, see output in .$file_log_build_docker_test"
        return 1
    fi
    #partie pylint
    printinfo "pylint running..."
    $dockerpypodorun --rm --entrypoint="pylint" pypodo_test pypodo/__pypodo__.py
        if [[ $? = 1 ]]
    then
        printerror "pylint ok, see output in $file_log_pylint"
        return 1
    else
        printinfo "pylint ko, see output in $file_log_pylint"
    fi
    printinfo "unittest running..."
    #partie unittest
    $dockerpypodorun --rm --entrypoint="python" pypodo_test -m unittest -v pypodo/__pypodo__test.py > $file_log_test
    if [[ $? = 0 ]]
    then
        printinfo "unittest ok, see output in $file_log_test"
    else
        printerror "unittest ko, see output in $file_log_test"
        return 1
    fi
    #partie coverage
    printinfo "coverage run running..."
    $dockerpypodorun --name pypodo_coverage --entrypoint="coverage" pypodo_test run 1>> $file_log_coverage 2>> $file_log_coverage
    if [[ $? = 0 ]]
    then
        printinfo "coverage run  ok, see output in $file_log_coverage"
    else
        printerror "coverage run  ko, see output in $file_log_coverage"
        return 1
    fi
    docker commit pypodo_coverage pypodo_coverage > /dev/null
    docker run -it --name pypodo_coverage_html --entrypoint="coverage" pypodo_coverage html
    docker cp pypodo_coverage_html:/pypodo/$folder_log_coverage .
    printinfo "coverage run  ok, see output in $folder_log_coverage/index.html"
    #partie mutatest
    if [[ $1 = "fast" ]]
    then
        printwarning "mutatest disabled"
    else
        printinfo "mutatest running..."
        $dockerpypodorun --name pypodo_mutation --entrypoint="mutatest" pypodo_test > /dev/null 2>> $file_log_mutation
        if [[ $? = 0 ]]
        then
            printinfo "coverage run  ok, see output in $file_log_mutation"
        else
            docker cp pypodo_mutation:/pypodo/$file_log_mutation .
            printerror "coverage run  ko, see output in $file_log_mutation"
            return 1
        fi
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
    $smoketest find "t.*che") > ci_cd/cache/log
    $smoketest backup > ci_cd/cache/log_backup
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


pipci () {
    #partie configuration
    printinfo "configuration running..."
    (rm -rf htmlcov/*
        rm *.log
        touch $file_log_coverage $file_log_mutation $file_log_configuration $install.log $file_log_test $file_log_pylint
        pip3 install mutatest
        pip3 install coverage
    pip3 install pylint) 1>> $file_log_configuration 2>> $file_log_configuration
    printinfo "configuration ok, see output in configuration.log"
    #partie pylint
    printinfo "pylint running..."
    pylint pypodo/__pypodo__.py  2> $file_log_pylint 1> $file_log_pylint
    if [[ $? = 1 ]]
    then
        printerror "pylint ko, see output in $file_log_pylint"
        return 1
    else
        printinfo "pylint ok, see output in $file_log_pylint"
    fi
    #partie unittest
    printinfo "unittest running..."
    python3 -m unittest -v pypodo/__pypodo__test.py 2> $file_log_test
    if [[ $? = 0 ]]
    then
        printinfo "unittest ok, see output in $file_log_test"
    else
        printerror "unittest ko, see output in $file_log_test"
        return 1
    fi
    #partie coverage
    printinfo "coverage run running..."
    coverage run 1>> $file_log_coverage 2>> $file_log_coverage
    if [[ $? = 0 ]]
    then
        printinfo "coverage run ok, see output in $file_log_coverage"
    else
        printerror "coverage run ko, see output in $file_log_coverage"
        return 1
    fi
    coverage html 2>&1 > /dev/null
    printinfo "coverage html running..."
    if [[ $? = 0 ]]
    then
        printinfo "coverage html, see output in $folder_log_coverage"
    else
        printerror "coverage html, see output in $folder_log_coverage"
        return 1
    fi
    #partie mutatest
    if [[ $1 = "fast" ]]
    then
        printwarning "mutatest disabled"
    else
        printinfo "mutatest running..."
        mutatest > /dev/null 2>> $file_log_mutation
        if [[ $? = 0 ]]
        then
            printinfo "mutatest ok, see output in $file_log_mutation"
        else
            printerror "mutatest ko, see output in $file_log_mutation"
            return 1
        fi
    fi
}

dockercd () {
    docker build -t pypodo . --no-cache 1>> $file_log_build_docker_prod 2>> $file_log_build_docker_prod
    if [[ $? = 0 ]]
    then
        printinfo "docker build ok, see output in $file_log_build_docker_prod "
    else
        printerror "docker build ko, see output in $file_log_build_docker_prod "
        return 1
    fi
}

pipcd () {
    #partie install
    printinfo "pip3 install running..."
    pip3 install --user . 2>> $file_log_install 1>> $file_log_install
    if [[ $? = 0 ]]
    then
        printinfo "pip3 install ok, see output in $file_log_install"
    else
        printerror "pip3 install ko, see output in $file_log_install"
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


if [[ $1 = "docker" ]]
then
    if [[ $2 = "ci" ]]
    then
        dockerci "$3"
        if [[ $? = 0 ]]
        then
            printinfo "docker ci ok"
        else
            printerror "docker ci ko"
        fi
    elif [[ $2 = "cd" ]]
    then
        dockerci "$3" && dockercd
        if [[ $? = 0 ]]
        then
            printinfo "docker ci_cd ok"
        else
            printerror "docker ci_cd ko"
            exit 1
        fi
    else
        printerror "ko - bad params : docker (ci/cd) [fast]"
    fi
    
elif [[ $1 = "pip" ]]
then
    if [[ $2 = "ci" ]]
    then
        pipci "$3"
        if [[ $? = 0 ]]
        then
            printinfo "pip ci ok"
        else
            printerror "pip ci ko"
            exit 1
        fi
    elif [[ $2 = "cd" ]]
    then
        pipci "$3" && pipcd
        if [[ $? = 0 ]]
        then
            printinfo "pip ci_cd ok"
        else
            printerror "pip ci_cd ko"
            exit 1
        fi
    else
        printerror "ko - bad params : pip (ci/cd) [fast]"
    fi
    
elif [[ $1 = "full" ]]
then
    dockerci $2 && dockercd && pipcd
    if [[ $? = 0 ]]
    then
        printinfo "CI_CD FULL OK"
    else
        printerror "CI_CD FULL KO"
        exit 1
    fi
else
    printerror "ko - bad params : (docker/pip) (ci/cd) [fast] or full [fast]"
fi
