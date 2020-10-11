#!/bin/bash
green="\e[32m"
red="\e[31m"


dockerci () {
    echo "*****DEBUT_CONFIGURATION_CLEAR******"
    docker rm pypodo_mutation
    docker rm pypodo_coverage
    docker rmi pypodo_coverage
    docker rmi pypodo_test
    docker rm pypodo_coverage_html
    docker rmi pypodo_coverage_html
    rm ci_cd/cache/.todo_mise_en_forme
    rm -rf htmlcov/*
    rm mutation.log
    export PYPODO_FILE=/tmp/.todo && touch $PYPODO_FILE && rm $PYPODO_FILE && touch $PYPODO_FILE
    export PYPODO_BACKUP=/tmp/.todo_backup && rm -rf $PYPODO_BACKUP && mkdir $PYPODO_BACKUP
    smoketest="docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup pypodo_test" &&\
    dockerpypodorun="docker run --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup -ti" &&\
    
    
    echo "*****FIN_CONFIGURATION_CLEAR******"
    echo "" &&\
    echo "" &&\
    echo "" &&\
    echo "*****DEBUT_DOCKER_BUILD******" &&\
    docker build -t pypodo_test . --no-cache &&\
    echo "*****FIN_DOCKER_BUILD******" &&\
    echo "" &&\
    echo "" &&\
    echo "" &&\
    echo "*****DEBUT_TU_TEST******" &&\
    #FIXME actually we have two commande to display the log AND save it AND exit if fail
    $dockerpypodorun --rm --entrypoint="python" pypodo_test -m unittest -v pypodo/__pypodo__test.py | tee "test.log" &&\
    $dockerpypodorun --rm --entrypoint="python" pypodo_test -m unittest -v pypodo/__pypodo__test.py > /dev/null &&\
    
    echo "*****FIN_TU_TEST******" &&\
    echo "" &&\
    echo "" &&\
    echo "" &&\
    echo "*****DEBUT_TU_COVERAGE******" &&\
    $dockerpypodorun --name pypodo_coverage --entrypoint="coverage" pypodo_test run &&\
    #FIXME actually we commit the container as an image to restart one other container and launch html...
    docker commit pypodo_coverage pypodo_coverage &&\
    docker run -it --name pypodo_coverage_html --entrypoint="coverage" pypodo_coverage html &&\
    docker cp pypodo_coverage_html:/pypodo/htmlcov . && echo "you can see the coverage in htmlcov folder" &&\
    echo "*****FIN_TU_COVERAGE******" &&\
    echo "" &&\
    echo "" &&\
    echo "" &&\
    echo "*****DEBUT_TU_MUTATION******" &&\
    if [[ $1 = "fast" ]]
    then
        echo -e "$red""mutatest disabled""\e[39m"
    else
        #FIXME no idea to otain full Number of location
        $dockerpypodorun --name pypodo_mutation --entrypoint="mutatest" pypodo_test &&\
        docker cp pypodo_mutation:/pypodo/mutation.log . && echo "you can see the coverage in mutation.log"
    fi &&\
    
    echo "*****FIN_TU_MUTATION******" &&\
    echo "" &&\
    echo "" &&\
    echo "" &&\
    echo "*****DEBUT_SMOKE_TEST******" &&\
    $smoketest list  &&\
    $smoketest add "tache1" &&\
    $smoketest add "tache2 #montag" &&\
    $smoketest add "tache3 #urgent" &&\
    $smoketest list && $smoketest del 2 &&\
    $smoketest tag montag2 3 &&\
    $smoketest tag urgente 3 &&\
    $smoketest sort &&\
    $smoketest add "mon autre tache #tag #retag" &&\
    $smoketest list tag retag &&\
    $smoketest untag retag 3 &&\
    $smoketest tag newtag 3 3 2 &&\
    $smoketest list &&\
    $smoketest tag &&\
    $smoketest untag &&\
    $smoketest find "t.*che" &&\
    $smoketest backup &&\
    echo "*****FIN_SMOKE_TEST******" &&\
    echo "" &&\
    echo "" &&\
    echo "" &&\
    echo "*****DEBUT_COMPARAISON_TODO******" &&\
    diff ${PYPODO_FILE} ci_cd/.todo.expected && echo "comparaison todo ok" &&\
    echo "*****FIN_COMPARAISON_TODO******" &&\
    echo "" &&\
    echo "" &&\
    echo "" &&\
    echo "*****DEBUT_VERIF_BACKUP_TODO******" &&\
    diff ${PYPODO_BACKUP}/.todo* ci_cd/.todo.expected && echo "comparaison backup ok" &&\
    echo "*****FIN_VERIF_BACKUP_TODO******" &&\
    echo "" &&\
    echo "" &&\
    echo "" &&\
    echo "*****DEBUT_VERIF_MISE_EN_FORME_TODO******" &&\
    $smoketest list > ci_cd/cache/.todo_mise_en_forme &&\
    diff ci_cd/cache/.todo_mise_en_forme ci_cd/.todo_mise_en_forme.expected && echo "comparaison mise en forme ok" &&\
    echo "*****FIN_VERIF_MISE_EN_FORME_TODO******"  &&\
    echo "*****DEBUT_VERIF_MISE_EN_FORME_LISTE_TAGS******" &&\
    $smoketest tag > ci_cd/cache/.tags_mise_en_forme &&\
    diff ci_cd/cache/.tags_mise_en_forme ci_cd/.tags_mise_en_forme.expected && echo "comparaison mise en forme ok" &&\
    echo "*****FIN_VERIF_MISE_EN_FORME_LISTE_TAGS******"
    echo "*****DEBUT_VERIF_MISE_EN_FORME_SEARCH******" &&\
    $smoketest find "t.*che" > ci_cd/cache/.search_mise_en_forme &&\
    diff ci_cd/cache/.search_mise_en_forme ci_cd/.search_mise_en_forme.expected && echo "comparaison mise en forme ok" &&\
    echo "*****FIN_VERIF_MISE_EN_FORME_SEARCH******"
}


pipci () {
    echo "*****DEBUT_CONFIGURATION_CLEAR******"
    rm -rf htmlcov/*
    rm mutation.log
    rm test.log
    pip3 install mutatest
    pip3 install coverage
    echo "*****FIN_CONFIGURATION_CLEAR******"
    python3 -m unittest -v pypodo/__pypodo__test.py 2>&1 | tee test.log &&\
    coverage run &&\
    coverage html &&\
    if [[ $1 = "fast" ]]
    then
        echo -e "$red""mutatest disabled""\e[39m"
    else
        mutatest
    fi
}

dockercd () {
    docker build -t pypodo . --no-cache
}

pipcd () {
    pip3 install --user .
}

if [[ $1 = "docker" ]]
then
    if [[ $2 = "ci" ]]
    then
        dockerci "$3"
        if [[ $? = 0 ]]
        then
            echo -e "$green""CI DOCKER OK""\e[39m"
        else
            echo -e "$red""CI DOCKER KO""\e[39m"
        fi
    elif [[ $2 = "cd" ]]
    then
        dockerci "$3" && dockercd
        if [[ $? = 0 ]]
        then
            echo -e "$green""CI_CD DOCKER OK""\e[39m"
        else
            echo -e "$red""CI_CD DOCKER KO""\e[39m"
        fi
    else
        echo -e "$red""KO - bad params : docker (ci/cd) [fast]""\e[39m"
    fi
    
elif [[ $1 = "pip" ]]
then
    if [[ $2 = "ci" ]]
    then
        pipci "$3"
        if [[ $? = 0 ]]
        then
            echo -e "$green""CI PIP OK""\e[39m"
        else
            echo -e "$red""CI PIP KO""\e[39m"
        fi
    elif [[ $2 = "cd" ]]
    then
        pipci "$3" && pipcd
        if [[ $? = 0 ]]
        then
            echo -e "$green""CI_CD PIP OK""\e[39m"
        else
            echo -e "$red""CI_CD PIP KO""\e[39m"
        fi
    else
        echo -e "$red""KO - bad params : pip (ci/cd) [fast]""\e[39m"
    fi
    
elif [[ $1 = "full" ]]
then
    dockerci $2 && dockercd && pipcd
    if [[ $? = 0 ]]
    then
        echo -e "$green""CI_CD FULL OK""\e[39m"
    else
        echo -e "$red""CI_CD FULL KO""\e[39m"
    fi
else
    echo -e "$red""KO - bad params : (docker/pip) (ci/cd) [fast] or full [fast]""\e[39m"
fi
