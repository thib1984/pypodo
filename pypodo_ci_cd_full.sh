#!/bin/bash
./pypodo_ci_cd_docker.sh &&\
echo "*****DEBUT_PIP_BUILD******" &&\
pip3 install --user . &&\
echo "*****FIN_PIP_BUILD******" &&\
echo "" &&\
echo "" &&\
echo ""

if [[ $? = 0 ]]
then
echo ""
echo ""
echo ""
echo "CI_CD FULL OK"
else
echo ""
echo ""
echo ""
echo "CI_CD FULL KO - ERROR"
exit 1
fi