#!/bin/bash
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_INSTALLATION******" &&\
pip3 install --user . &&\
echo "*****FIN_INSTALLATION******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_TEST******" &&\
python3 pypodo/__pypodo__test.py &&\
echo "*****FIN_TEST******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_COUVERTURE******" &&\
coverage run -m unittest pypodo/__pypodo__test.py &&\
coverage report &&\
echo "*****FIN_COUVERTURE******" &&\
echo "" &&\
echo "" &&\
echo "" &&\
echo "*****DEBUT_DOCKER_BUILD******" &&\
docker build -t pypodo . --no-cache &&\
echo "*****FIN_DOCKER_BUILD******" &&\
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
echo ""


if [[ $? = 0 ]]
then
echo ""
echo ""
echo ""
echo "CI_CD OK"
else
echo ""
echo ""
echo ""
echo "CI_CD KO - ERROR"
exit 1
fi