#!/bin/bash
echo "*****DEBUT_CONFIGURATION_CLEAR******"
docker rm coverage
docker rm coveragehtml
rm ci_cd/.todo_mise_en_forme
rm -rf htmlcov/*
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
echo "*****DEBUT_DOCKER_TEST******" &&\
docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup -ti --entrypoint="python" pypodo -m unittest -v pypodo/__pypodo__test.py &&\
echo "*****FIN_DOCKER_TEST******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_DOCKER_COVERAGE******" &&\
docker run --name coverage --mount type=bind,source=${PYPODO_FILE},target=/root/.todo --mount type=bind,source=${PYPODO_BACKUP},target=/root/.todo_backup -ti --entrypoint="coverage" pypodo run -m unittest pypodo/__pypodo__test.py &&\
docker commit coverage coverage &&\
docker run -it --entrypoint="coverage" coverage report &&\
docker run -it --name coveragehtml --entrypoint="coverage" coverage html &&\
docker commit coveragehtml coveragehtml &&\
docker cp coveragehtml:/pypodo/htmlcov . &&\
echo "*****FIN_DOCKER_COVERAGE******" &&\
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
echo "*****FIN_VERIF_MISE_EN_FORME_TODO******" &&\
if [[ $? = 0 ]]
then
echo ""
echo ""
echo ""
echo "CI_CD DOCKER OK"
else
echo ""
echo ""
echo ""
echo "CI_CD DOCKER KO - ERROR"
exit 1
fi