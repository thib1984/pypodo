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
    rm ./*.log 2> /dev/null
    touch $file_log_mutation
    (rm ci_cd/cache/*
        touch $file_log_coverage $file_log_build_docker_test $file_log_test $file_log_pylint $file_log_build_docker_prod
        docker rm pypodo_mutation
        docker rm pypodo_coverage
        docker rm pypodo_coverage_html
        docker rmi pypodo_coverage
        docker rmi thibaultgarcon/pypodo_test
        touch $PYPODO_FILE && rm $PYPODO_FILE && touch $PYPODO_FILE && touch $PYPODO_CONF && rm $PYPODO_CONF && touch $PYPODO_CONF && rm -rf $PYPODO_BACKUP && mkdir $PYPODO_BACKUP
    docker rmi pypodo_coverage_html) &>> $file_log_configuration
    printinfo "configuration finished, see output in $file_log_configuration"
    #build
    printinfo "docker build running..."
    if docker build -t thibaultgarcon/pypodo_test . --no-cache 1>>$file_log_build_docker_test 2>>$file_log_build_docker_test;
    then
        printinfo "docker build ok, see output in $file_log_build_docker_test"
    else
        printerror "docker build ko, see output in $file_log_build_docker_test"
        return 1
    fi
    #pylint
    printinfo "pylint running..."
    if $dockerpypodorun --rm --entrypoint="pylint" thibaultgarcon/pypodo_test pypodo/*.py 2>>$file_log_pylint 1> $file_log_pylint;
    then
        printinfo "pylint ok, see output in $file_log_pylint"
    else
        printerror "pylint ko, see output in $file_log_pylint"
        return 1
    fi
    printinfo "unittest running..."
    #unittest
    if $dockerpypodorun --rm --entrypoint="python" thibaultgarcon/pypodo_test -m unittest -v pypodo/__pypodo__test.py > $file_log_test
    then
        printinfo "unittest ok, see output in $file_log_test"
    else
        printerror "unittest ko, see output in $file_log_test"
        return 1
    fi
    #coverage
    printinfo "coverage run running..."
    if $dockerpypodorun --name pypodo_coverage --entrypoint="coverage" thibaultgarcon/pypodo_test run 1>> $file_log_coverage 2>> $file_log_coverage;
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
    #mutatest
    if [[ $1 = "fast" ]]
    then
        printwarning "mutatest disabled"
    else
        printinfo "mutatest running..."
        if $dockerpypodorun --name pypodo_mutation --entrypoint="mutatest" thibaultgarcon/pypodo_test > /dev/null 2>> $file_log_mutation;
        then
            printinfo "coverage run  ok, see output in $file_log_mutation"
        else
            docker cp pypodo_mutation:/pypodo/$file_log_mutation .
            printerror "coverage run  ko, see output in $file_log_mutation"
            return 1
        fi
    fi
    #end-to-end
    printinfo "test end-to-end 1/5 running... compare log"
    ./ci_cd/end_to_end.sh "$smoketest" > ci_cd/cache/log
    $smoketest backup > ci_cd/cache/log_backup
    if diff ci_cd/cache/log ci_cd/log.expected >> $file_log_end_to_end;
    then
        printinfo "test end-to-end 1/5 ok, see output in $file_log_end_to_end"
    else
        printerror "test end-to-end 1/5 ko, see output in $file_log_end_to_end"
        return 1
    fi
    printinfo "test end-to-end 2/5 running... compare backup log"
    if grep "\[32minfo    : creating todolist backup - .todo[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]" ci_cd/cache/log_backup >> $file_log_end_to_end;
    then
        printinfo "test end-to-end 2/5 ok, see output in $file_log_end_to_end"
    else
        printerror "test end-to-end 2/5 ko, see output in $file_log_end_to_end"
        return 1
    fi
    printinfo "test end-to-end 3/5 running... compare todofile"
    if diff ${PYPODO_FILE} ci_cd/.todo.expected >> $file_log_end_to_end;
    then
        printinfo "test end-to-end 3/5 ok, see output in $file_log_end_to_end"
    else
        printerror "test end-to-end 3/5 ko, see output in $file_log_end_to_end"
        return 1
    fi
    printinfo "test end-to-end 4/5 running... compare todobackupfile"
    if  diff ${PYPODO_BACKUP}/.todo* ci_cd/.todo.expected >> $file_log_end_to_end;
    then
        printinfo "test end-to-end 4/5 ok, see output in $file_log_end_to_end"
    else
        printerror "test end-to-end 4/5 ko, see output in $file_log_end_to_end"
        return 1
    fi
    printinfo "test end-to-end 5/5 running... compare log with special conf"
    rm "$PYPODO_FILE"
    touch "$PYPODO_FILE"
    cp ./ci_cd/.todo.rc $PYPODO_CONF
    ./ci_cd/end_to_end.sh "$smoketest" > ci_cd/cache/log.with.conf
    if diff ci_cd/cache/log.with.conf ci_cd/log.with.conf.expected >> $file_log_end_to_end;
    then
        printinfo "test end-to-end 5/5 ok, see output in $file_log_end_to_end"
    else
        printerror "test end-to-end 5/5 ko, see output in $file_log_end_to_end"
        return 1
    fi
}


pipci () {
    #configuration
    printinfo "configuration running..."
    (rm -rf htmlcov/*
        rm ./*.log
        touch $file_log_coverage $file_log_mutation $file_log_configuration $file_log_install $file_log_test $file_log_pylint
        pip3 install mutatest
        pip3 install coverage
    pip3 install pylint) 1>> $file_log_configuration 2>> $file_log_configuration
    printinfo "configuration ok, see output in configuration.log"
    #pylint
    printinfo "pylint running..."
    if pylint pypodo/*.py  2> $file_log_pylint 1> $file_log_pylint;
    then
        printinfo "pylint ok, see output in pylint.log"
    else
        printerror "pylint ko, see output in pylint.log"
        return 1
    fi
    #unittest
    printinfo "unittest running..."
    if python3 -m unittest -v pypodo/__pypodo__test.py 2> $file_log_test;
    then
        printinfo "unittest ok, see output in $file_log_test"
    else
        printerror "unittest ko, see output in $file_log_test"
        return 1
    fi
    #coverage
    printinfo "coverage run running..."
    if coverage run 1>> $file_log_coverage 2>> $file_log_coverage;
    then
        printinfo "coverage run ok, see output in $file_log_coverage"
    else
        printerror "coverage run ko, see output in $file_log_coverage"
        return 1
    fi
    printinfo "coverage html running..."
    if coverage html > /dev/null 2>&1;
    then
        printinfo "coverage html, see output in $folder_log_coverage"
    else
        printerror "coverage html, see output in $folder_log_coverage"
        return 1
    fi
    #mutatest
    if [[ $1 = "fast" ]]
    then
        printwarning "mutatest disabled"
    else
        printinfo "mutatest running..."
        if mutatest > /dev/null 2>> $file_log_mutation;
        then
            printinfo "mutatest ok, see output in $file_log_mutation"
        else
            printerror "mutatest ko, see output in $file_log_mutation"
            return 1
        fi
    fi
}

dockercd () {
    if docker build -t thibaultgarcon/pypodo:latest . --no-cache 1>> $file_log_build_docker_prod 2>> $file_log_build_docker_prod;
    then
        printinfo "docker build ok, see output in $file_log_build_docker_prod "
    else
        printerror "docker build ko, see output in $file_log_build_docker_prod "
        return 1
    fi
}

pipcd () {
    #install
    printinfo "pip3 install running..."
    if pip3 install --user . 2>> $file_log_install 1>> $file_log_install;
    then
        printinfo "pip3 install ok, see output in $file_log_install"
    else
        printerror "pip3 install ko, see output in $file_log_install"
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


if [[ $1 = "docker" ]]
then
    if [[ $2 = "ci" ]]
    then
        if dockerci "$3";
        then
            printinfo "docker ci ok"
        else
            printerror "docker ci ko"
            exit 1
        fi
    elif [[ $2 = "cd" ]]
    then
        if dockerci "$3" && dockercd;
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
        if pipci "$3";
        then
            printinfo "pip ci ok"
        else
            printerror "pip ci ko"
            exit 1
        fi
    elif [[ $2 = "cd" ]]
    then
        if pipci "$3" && pipcd;
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
    if dockerci "$2" && dockercd && pipcd;
    then
        printinfo "full ci_cd ok"
    else
        printerror "full ci_cd ko"
        exit 1
    fi
else
    printerror "ko - bad params : (docker/pip) (ci/cd) [fast] or full [fast]"
fi
