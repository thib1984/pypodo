#!/bin/bash
docker rm coverage
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_DOCKER_BUILD******" &&\
docker build -t pypodo . --no-cache &&\
export PYPODO_FILE=/tmp/.todo && touch $PYPODO_FILE && rm $PYPODO_FILE && touch $PYPODO_FILE &&\
echo "*****FIN_DOCKER_BUILD******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_DOCKER_TEST******" &&\
docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo  -ti --entrypoint="python" pypodo -m unittest -v pypodo/__pypodo__test.py &&\
echo "*****FIN_DOCKER_TEST******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****
DEBUT_DOCKER_COVERAGE******" &&\
docker run --name coverage --mount type=bind,source=${PYPODO_FILE},target=/root/.todo  -ti --entrypoint="coverage" pypodo run -m unittest pypodo/__pypodo__test.py &&\
docker commit coverage coverage &&\
docker run -it --entrypoint="coverage" coverage report &&\
echo "*****FIN_DOCKER_COVERAGE******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_CONFIG_SMOKE_TEST******" &&\
export PYPODO_FILE=/tmp/.todo && touch $PYPODO_FILE && rm $PYPODO_FILE && touch $PYPODO_FILE && smoketest="docker run --rm --mount type=bind,source=${PYPODO_FILE},target=/root/.todo pypodo" &&\
echo "*****FIN_CONFIG_SMOKE_TEST******" &&\
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
echo "*****FIN_SMOKE_TEST******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_COMPARAISON_TODO******" &&\
diff ${PYPODO_FILE} ci_cd/.todo.expected &&\
echo "*****FIN_COMPARAISON_TODO******" &&\
echo "" &&\
echo "" &&\
echo "" &&\

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