#!/bin/bash
green="\e[32m"
red="\e[31m"


dockerci () {
echo "*****DEBUT_CONFIGURATION_CLEAR******"
docker rm mutation
docker rm coverage
docker rm coveragehtml
rm ci_cd/.todo_mise_en_forme
rm -rf htmlcov/*
rm mutation.log
echo "*****FIN_CONFIGURATION_CLEAR******" 
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_DOCKER_BUILD******" &&\
docker build -t pypodo . --no-cache &&\
export PYPODO_FILE=/tmp/.todo && touch $PYPODO_FILE && rm $PYPODO_FILE && touch $PYPODO_FILE &&\
export PYPODO_BACKUP=/tmp/.todo_backup && rm -rf $PYPODO_BACKUP && mkdir $PYPODO_BACKUP &&\  
smoketest="docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup pypodo" &&\
echo "*****FIN_DOCKER_BUILD******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_TU_TEST******" &&\
(docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup -ti --entrypoint="python" pypodo -m unittest -v pypodo/__pypodo__test.py | tee "test.log") &&\
docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup -ti --entrypoint="python" pypodo -m unittest -v pypodo/__pypodo__test.py > /dev/null &&\

echo "*****FIN_TU_TEST******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_TU_COVERAGE******" &&\
docker run --name coverage --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup -ti --entrypoint="coverage" pypodo run -m unittest pypodo/__pypodo__test.py &&\
docker commit coverage coverage &&\
docker run -it --entrypoint="coverage" coverage report &&\
docker run -it --name coveragehtml --entrypoint="coverage" coverage html &&\
docker commit coveragehtml coveragehtml &&\
docker cp coveragehtml:/pypodo/htmlcov . && echo "you can see the coverage in htmlcov folder" &&\
echo "*****FIN_TU_COVERAGE******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_TU_MUTATION******" &&\
docker run --name mutation --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup -ti --entrypoint="mutatest" pypodo --src pypodo/__pypodo__.py -t "python3 -m unittest -v pypodo/__pypodo__test.py" -o mutation.log &&\
docker cp mutation:/pypodo/mutation.log . && echo "you can see the coverage in mutation.log" &&\
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
$smoketest untag retag 3 &&\
$smoketest tag newtag 3 3 2 &&\
$smoketest list &&\
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
echo "*****FIN_VERIF_MISE_EN_FORME_TODO******"
} 


pipci () {
echo "*****DEBUT_CONFIGURATION_CLEAR******"
rm -rf htmlcov/*
rm mutation.log
rm test.log
echo "*****FIN_CONFIGURATION_CLEAR******" 
python3 -m unittest -v pypodo/__pypodo__test.py 2>&1 | tee test.log &&\
coverage run -m unittest pypodo/__pypodo__test.py &&\
coverage report &&\
coverage html &&\
mutatest --src pypodo/__pypodo__.py  -t "python3 -m unittest -v pypodo/__pypodo__test.py" -o mutation.log
}

pipcd () {
pip3 install --user .
}

if [[ $1 = "docker" ]]
then
dockerci
if [[ $? = 0 ]]
then
echo -e "$green""CI DOCKER OK""\e[39m"
else
echo -e "$red""CI DOCKER KO""\e[39m"
fi

elif [[ $1 = "pip" ]]
then
pipci && pipcd
if [[ $? = 0 ]]
then
echo -e "$green""CI CD PIP OK""\e[39m"
else
echo -e "$red""CI CD PIP KO""\e[39m"
fi

elif [[ $1 = "full" ]]
then
dockerci && pipcd
if [[ $? = 0 ]]
then
echo -e "$green""CI DOCKER CD PIP OK""\e[39m"
else
echo -e "$red""CI DOCKER CD PIP KO""\e[39m"
fi

else
echo -e "$red""KO Bad Parameter""\e[39m"
fi
